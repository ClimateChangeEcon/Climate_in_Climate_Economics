using XLSX, Plots

function cc(em)
   x=zeros(3)
   x[1]=(1.0-b12)*m[1]+b12*meq[1]/meq[2]*m[2]+em
   x[2]=b12*m[1]+(1.0-b12*meq[1]/meq[2]-b23)*m[2]+b23*meq[2]/meq[3]*m[3]
   x[3]=b23*m[2]+(1-b23*meq[2]/meq[3])*m[3]
   return x
end

function tep(f)
   x=zeros(2)
   x[1]=t[1]+c1*f-c1*forcing/ecs*t[1]-c1*c3*(t[1]-t[2])
   x[2]=t[2]+c4*(t[1]-t[2])
   return x
end

function damage(temp)
  return   ps1*temp+ps2*temp^2+ps3*temp^3
end

function disdam(f)
   global m[:]=m0
   global t[:]=t0
   dam=0.0
   for i=1:capt
      force=forcing*log(m[1]/meq[1])/log(2.0) #+0.5+min(0.5,i/(2*85))
#      if nordy == 0
#         if f == 0
#            cdice[i,2]=force*0.3
#            force=force*1.3
#         else
#            force=force+cdice[i,2]
#         end
#      else
         force= force+0.5+0.5*min(i,85)/85.0
#      end
      global m=cc(emission[i])
      global t=tep(force)
      global cdice[i,1]=i
#      global cdice[i,2]=t[1] # force # damage(t[1])*magic^i
      if i < horizon
         dam += damage(t[1]) *magic^i
      else
         dam += damage(t[1]) *0.95^i
      end
      # println(force)
    end
   return dam
end

function scc(l)
   cost=0.0
   dama= disdam(0)/(magic^tau)
#   hdice[:,l]=cdice[:,2] # (cdice[:,2]-hdice[:,l])/pulse
   global emission[tau]+=pulse
   global hdice[:,l]=cdice[:,2]
   dama2=disdam(1)/(magic^tau)
   global emission[tau]+= -pulse
   cost=(dama2-dama)/pulse
   return cost
end

function mmmtem()
   global t0=[1.10; 0.27]
   global c1=0.137
   global c3=0.73
   global c4=0.00689
   global forcing=3.45
   global ecs=3.25
end
function mmmcc()
   global m0=[851.0; 628.0; 1323.0]
   global b12=0.054
   global b23=0.0082
   global meq=[607.0; 489.0; 1281.0]
end
function hecs()
   global t0=[1.10; 0.26]
   global c1=0.154
   global c3=0.55
   global c4=0.00671
   global ecs=4.55
   global forcing=2.95
end
function lecs()
   global t0=[1.10; 0.34]
   global c1=0.213
   global c3=1.16
   global c4=0.00921
   global ecs=2.15
   global forcing= 3.65
end

function LOVE()
 global b12=0.067
 global b23=0.0095
 global meq=[607.0; 600.0;  1385.0]
 global m0=[850, 770, 1444]
 global t0=[1.10; 0.27]
end

function MESMO()
   # Extreme high CC
    global b12=0.059
    global b23=0.008
    global meq=[607.0; 305.0;  865.0]
    global m0=[851.0; 403.0; 894.0]
    global t0=[1.10; 0.27]
end

global m0=[851.0; 628.0; 1323.0]
global t0=[1.10; 0.27]
global b12=0.054
global b23=0.0082
global meq=[607.0; 489.0; 1281.0]
global c1=0.137
global c3=0.73
global c4=0.00689
global forcing=3.45
global ecs=3.25
global m=m0
global t=t0
global ps1=0.0
global ps2=0.01#025
global ps3=0.0#11 1/7^7
const capt=2000
global horizon=capt
global tau=5
const pulse=1.0
global emission=zeros(capt)
global magic=1.0
global emission[1:300]=XLSX.readdata("./BAU_emissions_vsRCP.xlsx","Лист1!G2:G301")
# load emissions RCP 8.5 from Excel file
global cdice=ones(capt,2)
global hdice=zeros(capt,10)
global nordy=0

global z=zeros(50,11)
global bench=zeros(50)
for t=1:50
   global magic=0.96+(t-1)/50*0.035
   global z[t,1]=1.0/magic
   global bench[t]=scc(1)
end


for t=1:50
   global magic=0.96+(t-1)/50*0.035
   global z[t,2]=scc(1)/bench[t]
end



hecs()

  for t=1:50
    global magic=0.96+(t-1)/50*0.035
    global z[t,3]=scc(1)/bench[t]
  end

 mmmtem()
 lecs()

 for t=1:50
   global magic=0.96+(t-1)/50*0.035
   global z[t,4]=scc(1)/bench[t]
 end

mmmtem()
global ecs=4.55
for t=1:50
  global magic=0.96+(t-1)/50*0.035
  global z[t,5]=scc(1)/bench[t]
end

mmmtem()
global ecs=2.15

for t=1:50
  global magic=0.96+(t-1)/50*0.035
  global z[t,6]=scc(1)/bench[t]
end


mmmcc()
mmmtem()


# DICE 2016
# these are the parameters reported for DICE 2016

 global b12=0.024
 global b23=0.0014
 global meq=[588.0; 360.0; 1720.0]
 global m0=[851; 460; 1740]
 global c1=0.0201
 global c3=0.088
 global c4=0.005
 global forcing=3.6813
 global ecs=3.1
global t0=[0.85; 0.0068]
 for t=1:50
    global magic=0.96+(t-1)/50*0.035
    global z[t,7]=scc(1)/bench[t]
  end

global ecs=4.55
  for t=1:50
     global magic=0.96+(t-1)/50*0.035
     global z[t,8]=scc(1)/bench[t]
   end

 global ecs=2.15
 for t=1:50
    global magic=0.96+(t-1)/50*0.035
    global z[t,9]=scc(1)/bench[t]
  end



display(plot(z[:,1],z[:,2:9],xlabel="g-adjusted interest rate", ylabel="SCC relative to CDICE",minorticks=:true,
line = [:solid :solid :solid :dashdotdot :dashdotdot :dash :dash :dash ],
color =[:blue :red :black :red :black :blue :red :black ],
label=["CDICE" "CDICE-HadGEM2-ES" "CDICE-GISS-E2-R" "ecs45-CDICE"  "ecs21-CDICE" "DICE2016" "ecs45-DICE2016" "ecs21-DICE2016"]))


# label=["HadGEM2-MMM" "HadGEM2-MESMO" "GISS-MMM" "GISS-LOVECLIM" "DIC16" "DICE16-LECS" "DICE16-HECS"]))

# display(plot(cdice[1:300,1],hdice[1:300,1:2]))


savefig("figs/fig_10")
