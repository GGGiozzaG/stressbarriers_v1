# -*- coding: utf-8 -*-
"""
Differential Anisotropy Maps - Two layers case

- This script compare variations in barrier prediction between two anisotropic layers
- Each layer has constant thickness. We define, for each layer:
    SD (m)
    C33 (GPa)
    C44 (GPa)
    Ks (GPa)
- We define for both layers:
    SVG (MPa/m)
    PPSVGratio (-)
- We use the following variable definitions (only for top layer):
    Sh(psi)
    SH(psi)
- We use the following variable definitions (for each layer):
    Eps(-)
    Delta(-)
    Gamma(-)
    DEps(-)
    DDelta(-)
    DGamma(-)
- We calculate the tectonic strains using the parameters from the top layer
- We calculate Sh and SH columns
- We map stress polygons. Color code within stress polygons represent stress
variations due to differential anisotropy within layers.
- We plot stresses, stress gradients and stress gradients semblance
"""

    
#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

from ipywidgets import interact
from ipywidgets import SelectionSlider
SV=np.linspace(0,1,40)
PP=np.linspace(0,1,40)
C33=np.linspace(0,1,40)
C44=np.linspace(0,1,40)
C11=np.linspace(0,1,40)
C66=np.linspace(0,1,40)
C13=np.linspace(0,1,40)
C11_D=np.linspace(0,1,40)
C66_D=np.linspace(0,1,40)
C13_D=np.linspace(0,1,40)
Ks=np.linspace(0,1,40)
Eps=np.linspace(0,1,40)
Delta=np.linspace(0,1,40)
Gamma=np.linspace(0,1,40)
Eta=np.linspace(0,1,40)
Eta_D=np.linspace(0,1,40)
DEps=np.linspace(0,1,40)
DDelta=np.linspace(0,1,40)
DGamma=np.linspace(0,1,40)
Bioth=np.linspace(0,1,40)
Biotv=np.linspace(0,1,40)
Bioth_D=np.linspace(0,1,40)
Biotv_D=np.linspace(0,1,40)
Sh=np.linspace(0,1,40)
SH=np.linspace(0,1,40)
Sh_D=np.linspace(0,1,40)
SH_D=np.linspace(0,1,40)
DiffSV=np.linspace(0,1,40)
DiffPP=np.linspace(0,1,40)
DiffSmin=np.linspace(0,1,40)
DiffSmax=np.linspace(0,1,40)

C33_top=1000000000
C44_top=500000000
C33_bot=1000000000
C44_bot=500000000
Ks_top=100000000
Ks_bot=100000000
#Interactive parameters are: Epsilon, Delta, Gamma (Top and Bottom) and Shmin and difference to Shmax
def mkSlider(minX,maxX,step):
    values=[i*step for i in range(int(minX),int((maxX-minX)/step))]
    nuSlider = SelectionSlider(options=[("%g"%i,i) for i in values])
    return nuSlider
@interact(Eps_top=mkSlider(0,0.5,0.02),
          Eps_bot=mkSlider(0,0.5,0.02),
          Delta_top=mkSlider(0,0.5,0.02),
          Delta_bot=mkSlider(0,0.5,0.02),
          Gamma_top=mkSlider(0,0.5,0.02),
          Gamma_bot=mkSlider(0,0.5,0.02),
          DEps_top=mkSlider(0,0.5,0.02),
          DEps_bot=mkSlider(0,0.5,0.02),
          DDelta_top=mkSlider(0,0.5,0.02),
          DDelta_bot=mkSlider(0,0.5,0.02),
          DGamma_top=mkSlider(0,0.5,0.02),
          DGamma_bot=mkSlider(0,0.5,0.02),
          Sh_cal=mkSlider(0,1.5,0.02),
          dSh_cal=mkSlider(0,1.5,0.02)) # Widget variables 

def Stresses(Eps_top=0,Eps_bot=0,Delta_top=0,Delta_bot=0,Gamma_top=0,Gamma_bot=0,DEps_top=0,DEps_bot=0,DDelta_top=0,DDelta_bot=0,DGamma_top=0,DGamma_bot=0,Sh_cal=1,dSh_cal=0):  
    SD=2000                             #Depth in m
    Depth=np.linspace(SD,SD+20,40)
    index=0      #Depth column in m
    for d in Depth:
        SV[index]=2*d
        PP[index]=0.8*SV[index]
        if (index<40):
            C33[index]=C33_top
            C44[index]=C44_top
            Ks[index]=Ks_top
            Eps[index]=Eps_top
            Delta[index]=Delta_top
            Gamma[index]=Gamma_top
            DEps[index]=DEps_top
            DDelta[index]=DDelta_top
            DGamma[index]=DGamma_top
        elif (index<41):
            C33[index]=(C33_top+C33_bot)/2
            C44[index]=(C44_top+C44_bot)/2
            Ks[index]=(Ks_top+Ks_bot)/2
            Eps[index]=(Eps_top+Eps_bot)/2
            Delta[index]=(Delta_top+Delta_bot)/2
            Gamma[index]=(Gamma_top+Gamma_bot)/2
            DEps[index]=(DEps_top+DEps_bot)/2
            DDelta[index]=(DDelta_top+DDelta_bot)/2
            DGamma[index]=(DGamma_top+DGamma_bot)/2
        else:
            C33[index]=C33_bot
            C44[index]=C44_bot
            Ks[index]=Ks_bot
            Eps[index]=Eps_bot
            Delta[index]=Delta_bot
            Gamma[index]=Gamma_bot    
            DEps[index]=DEps_bot
            DDelta[index]=DDelta_bot
            DGamma[index]=DGamma_bot
            Eta[index]=(Eps[index]-Delta[index])/(1+2*Delta[index])
            C11[index]=C33[index]*(1+2*Eps[index])
            C66[index]=C44[index]*(1+2*Gamma[index])
            C13[index]=-C44[index]+np.sqrt((C33[index]-C44[index])**2+2*Delta[index]*(C33[index]**2-C33[index]*C44[index]))
            Eta_D[index]=((Eps[index]+DEps[index])-(Delta[index]+DDelta[index]))/(1+2*(Delta[index]+DDelta[index]))
            C11_D[index]=C33[index]*(1+2*(Eps[index]+DEps[index]))
            C66_D[index]=C44[index]*(1+2*(Gamma[index]+DGamma[index]))
            C13_D[index]=-C44[index]+np.sqrt((C33[index]-C44[index])**2+2*(Delta[index]+DDelta[index])*(C33[index]**2-C33[index]*C44[index]))
            Bioth[index]=1-(2*C11[index]-2*C66[index]+C13[index])/(3*Ks[index])
            Biotv[index]=1-(2*C13[index]+C33[index])/(3*Ks[index])
            Bioth_D[index]=1-(2*C11_D[index]-2*C66_D[index]+C13_D[index])/(3*Ks[index])
            Biotv_D[index]=1-(2*C13_D[index]+C33[index])/(3*Ks[index])

    SH_cal=(Sh_cal+dSh_cal)*SV[0]
    Sh_cal=Sh_cal*SV[0]
    K_SigmaV=C13[0]/C33[0]*SD
    K_S=(C33[0]-C13[0]**2/C33[0])
    K_Pp=PP[0]*(1-C13[0]/C33[0]+2/(3*Ks[0])*(-C33[0]+C44[0]+C13[0]**2/C33[0]))
    TSMax=(Sh_cal-K_SigmaV-K_Pp+K_S/(2*C44[0])*(SH_cal-Sh_cal))/(2*(K_S-C44[0]))
    TSMin=(Sh_cal-K_SigmaV-K_Pp-TSMax*(K_S-2*C44[0]))/K_S
    K_SigmaV_D=C13_D[0]/C33[0]*SD
    K_S_D=(C33[0]-C13_D[0]**2/C33[0])
    K_Pp_D=PP[0]*(1-C13_D[0]/C33[0]+2/(3*Ks[0])*(-C33[0]+C44[0]+C13_D[0]**2/C33[0]))
    TSMax_D=(Sh_cal-K_SigmaV_D-K_Pp_D+K_S_D/(2*C44[0])*(SH_cal-Sh_cal))/(2*(K_S_D-C44[0]))
    TSMin_D=(Sh_cal-K_SigmaV_D-K_Pp_D-TSMax_D*(K_S_D-2*C44[0]))/K_S_D

    index=0

    for d in Depth:
        Sh[index]=(C13[index]/C33[index])*(SV[index]-Biotv[index]*PP[index])-(C13[index]**2/C33[index])*(TSMin+TSMax)+C11[index]*(TSMin+TSMax)-2*C66[index]*(TSMax)+Bioth[index]*PP[index]
        SH[index]=(C13[index]/C33[index])*(SV[index]-Biotv[index]*PP[index])-(C13[index]**2/C33[index])*(TSMin+TSMax)+C11[index]*(TSMin+TSMax)-2*C66[index]*(TSMin)+Bioth[index]*PP[index]
        Sh_D[index]=(C13_D[index]/C33[index])*(SV[index]-Biotv_D[index]*PP[index])-(C13_D[index]**2/C33[index])*(TSMin+TSMax)+C11_D[index]*(TSMin_D+TSMax_D)-2*C66_D[index]*(TSMax_D)+Bioth_D[index]*PP[index]
        SH_D[index]=(C13_D[index]/C33[index])*(SV[index]-Biotv_D[index]*PP[index])-(C13_D[index]**2/C33[index])*(TSMin+TSMax)+C11_D[index]*(TSMin_D+TSMax_D)-2*C66_D[index]*(TSMin_D)+Bioth_D[index]*PP[index]
        DiffSV[index]=-(C13[index]-C13_D[index])/C33[index]*SV[index]
        DiffPP[index]=PP[index]*((C13[index]-C13_D[index])/C33[index]+2/3*1/Ks[index]*(-C13[index]+C13_D[index])/C33[index]*(C13[index]+C13_D[index]))+4*PP[index]/(3*Ks[index])*(DGamma[index]*C44[index]-DEps[index]*C33[index])
        #DiffSmin[index]=-(C13_D[index]**2/C33[index])*(TSMin+TSMax)+C11_D[index]*(TSMin_D+TSMax_D)-2*C66_D[index]*(TSMax_D)+(C13[index]**2/C33[index])*(TSMin+TSMax)(TSMin+TSMax)-C11[index]*(TSMin+TSMax)+2*C66[index]*(TSMax)
        #DiffSmax[index]=-(C13_D[index]**2/C33[index])*(TSMin+TSMax)+C11_D[index]*(TSMin_D+TSMax_D)-2*C66_D[index]*(TSMin_D)+(C13[index]**2/C33[index])*(TSMin+TSMax)(TSMin+TSMax)-C11[index]*(TSMin+TSMax)+2*C66[index]*(TSMin)
    
    
"""
Spyder Editor

This is a temporary script file.

Model.Sminimum=(Model.SV-Model.Biotiso*Model.PPRS)/3+Model.PPRS*Model.Biotiso;
Model.Sminimum_ani=(Model.SV-Model.Biotv*Model.PPRS)/3+Model.PPRS*Model.Bioth;
Model.Smaximum=(Model.SV-Model.Biotiso*Model.PPRS)*3+Model.PPRS*Model.Biotiso;
Model.Smaximum_ani=(Model.SV-Model.Biotv*Model.PPRS)*3+Model.PPRS*Model.Bioth;
Model.SmaxSVfraction=linspace(Model.Sminimum,Model.Smaximum,300);
Model.SminSVfraction=linspace(Model.Sminimum,Model.Smaximum,300);

Model.CasesSV=-(Model.C13_iso-Model.C13)/Model.C33*Model.SV;
Model.CasesPP=Model.PPRS*((Model.C13_iso-Model.C13)/Model.C33+2/3*1/Model.Ks*(-Model.C13_iso+Model.C13)/Model.C33*(Model.C13_iso+Model.C13))+4*Model.PPRS/(3*Model.Ks)*(Model.Gamma*Model.C44-Model.Eps*Model.C33);
Model.Case1_Sh=0.75e4;
Model.Case1_SH=0.8e4;

Model.Case1_DiffSminEpsGamma=Model.Case1_TSMax*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case1_TSMin*(2*Model.Eps*Model.C33);
Model.Case1_DiffSmaxEpsGamma=Model.Case1_TSMin*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case1_TSMax*(2*Model.Eps*Model.C33);
Model.Case1_Delta=(Model.Case1_TSMax+Model.Case1_TSMin)*(Model.C13_iso-Model.C13)/Model.C33*(Model.C13_iso+Model.C13);
Model.Case1_DiffSmin=Model.CasesSV+Model.CasesPP+Model.Case1_DiffSminEpsGamma+Model.Case1_Delta;
Model.Case1_DiffSmax=Model.CasesSV+Model.CasesPP+Model.Case1_DiffSmaxEpsGamma+Model.Case1_Delta;
Model.Case1_Sh_ani=Model.Case1_Sh+Model.Case1_DiffSmin;
Model.Case1_SH_ani=Model.Case1_SH+Model.Case1_DiffSmax;
Model.Case2_Sh=0.875e4;
Model.Case2_SH=0.95e4;
Model.Case2_TSMax=(Model.Case2_Sh-Model.K_SigmaV-Model.K_Pp+Model.K_S/(2*Model.C44)*(Model.Case2_SH-Model.Case2_Sh))/(2*(Model.K_S-Model.C44));
Model.Case2_TSMin=(Model.Case2_Sh-Model.K_SigmaV-Model.K_Pp-Model.Case2_TSMax*(Model.K_S-2*Model.C44))/Model.K_S;
Model.Case2_DiffSminEpsGamma=Model.Case2_TSMax*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case2_TSMin*(2*Model.Eps*Model.C33);
Model.Case2_DiffSmaxEpsGamma=Model.Case2_TSMin*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case2_TSMax*(2*Model.Eps*Model.C33);
Model.Case2_Delta=(Model.Case2_TSMax+Model.Case2_TSMin)*(Model.C13_iso-Model.C13)/Model.C33*(Model.C13_iso+Model.C13);
Model.Case2_DiffSmin=Model.CasesSV+Model.CasesPP+Model.Case2_DiffSminEpsGamma+Model.Case2_Delta;
Model.Case2_DiffSmax=Model.CasesSV+Model.CasesPP+Model.Case2_DiffSmaxEpsGamma+Model.Case2_Delta;
Model.Case2_Sh_ani=Model.Case2_Sh+Model.Case2_DiffSmin;
Model.Case2_SH_ani=Model.Case2_SH+Model.Case2_DiffSmax;
Model.Case3_Sh=0.85e4;
Model.Case3_SH=1.3e4;
Model.Case3_TSMax=(Model.Case3_Sh-Model.K_SigmaV-Model.K_Pp+Model.K_S/(2*Model.C44)*(Model.Case3_SH-Model.Case3_Sh))/(2*(Model.K_S-Model.C44));
Model.Case3_TSMin=(Model.Case3_Sh-Model.K_SigmaV-Model.K_Pp-Model.Case3_TSMax*(Model.K_S-2*Model.C44))/Model.K_S;
Model.Case3_DiffSminEpsGamma=Model.Case3_TSMax*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case3_TSMin*(2*Model.Eps*Model.C33);
Model.Case3_DiffSmaxEpsGamma=Model.Case3_TSMin*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.Case3_TSMax*(2*Model.Eps*Model.C33);
Model.Case3_Delta=(Model.Case3_TSMax+Model.Case3_TSMin)*(Model.C13_iso-Model.C13)/Model.C33*(Model.C13_iso+Model.C13);
Model.Case3_DiffSmin=Model.CasesSV+Model.CasesPP+Model.Case3_DiffSminEpsGamma+Model.Case3_Delta;
Model.Case3_DiffSmax=Model.CasesSV+Model.CasesPP+Model.Case3_DiffSmaxEpsGamma+Model.Case3_Delta;
Model.Case3_Sh_ani=Model.Case3_Sh+Model.Case3_DiffSmin;
Model.Case3_SH_ani=Model.Case3_SH+Model.Case3_DiffSmax;

%Sigma V coefficient

for j=1:length(Model.SmaxSVfraction)
    for k=1:length(Model.SminSVfraction)
        if Model.SmaxSVfraction(j)<Model.SminSVfraction(k)
            Model.TStrainmax(j,k)=NaN;
            Model.TStrainmin(j,k)=NaN;
        else
        %Tectonic Strain (Max)
            Model.TStrainmax(j,k)=(Model.SminSVfraction(k)-Model.K_SigmaV-Model.K_Pp+Model.K_S/(2*Model.C44)*(Model.SmaxSVfraction(j)-Model.SminSVfraction(k)))/(2*(Model.K_S-Model.C44));
        %Tectonic Strain (Max)
            Model.TStrainmin(j,k)=(Model.SminSVfraction(k)-Model.K_SigmaV-Model.K_Pp-Model.TStrainmax(j,k)*(Model.K_S-2*Model.C44))/Model.K_S;
        end
        if Model.SmaxSVfraction(j)>=Model.SV
            if Model.SmaxSVfraction(j)>(Model.SminSVfraction(k)-Model.Biotiso*Model.PPRS)*3+Model.PPRS*Model.Biotiso
                Model.TStrainmax(j,k)=NaN;
                Model.TStrainmin(j,k)=NaN;
            end
        end
%             if Model.TStrainmin(j,k)<=0
%                 Model.TStrainmin(j,k)=NaN;
%                 Model.TStrainmax(j,k)=NaN;
%             end
        %Minimum Stress Field
            Model.SHMin(j,k)=Model.K_SigmaV+Model.TStrainmin(j,k)*Model.K_S+Model.TStrainmax(j,k)*(Model.K_S-2*Model.C44)+Model.K_Pp;
        %Maximum Stress Field
            Model.SHMax(j,k)=Model.K_SigmaV+Model.TStrainmax(j,k)*Model.K_S+Model.TStrainmin(j,k)*(Model.K_S-2*Model.C44)+Model.K_Pp;
            Model.Tau(j,k)=(Model.TStrainmax(j,k)-Model.TStrainmin(j,k))/Model.TStrainmax(j,k);
        %Differential Vertical Stresses
            DiffSigmaV(j,k)=-(Model.C13_iso-Model.C13)/Model.C33*Model.SV;
        %Differential Tectonic Stresses
            %Epsilon-Gamma component
            DiffSigmaSminEpsGamma(j,k)=Model.TStrainmax(j,k)*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.TStrainmin(j,k)*(2*Model.Eps*Model.C33);
            DiffSigmaSmaxEpsGamma(j,k)=Model.TStrainmin(j,k)*(2*Model.Eps*Model.C33-4*Model.Gamma*Model.C44)+Model.TStrainmax(j,k)*(2*Model.Eps*Model.C33);
            DiffSigmaSDelta(j,k)=(Model.TStrainmax(j,k)+Model.TStrainmin(j,k))*(Model.C13_iso-Model.C13)/Model.C33*(Model.C13_iso+Model.C13);
            DiffSigmaSmin(j,k)=DiffSigmaSminEpsGamma(j,k)+DiffSigmaSDelta(j,k);
            DiffSigmaSmax(j,k)=DiffSigmaSmaxEpsGamma(j,k)+DiffSigmaSDelta(j,k);
        %Differential Pore Pressure Stresses
            DiffSigmaPpEpsGamma(j,k)=4*Model.PPRS/(3*Model.Ks)*(Model.Gamma*Model.C44-Model.Eps*Model.C33);
            DiffSigmaPpDelta(j,k)=Model.PPRS*((Model.C13_iso-Model.C13)/Model.C33+2/3*1/Model.Ks*(-Model.C13_iso+Model.C13)/Model.C33*(Model.C13_iso+Model.C13));
            DiffSigmaPp(j,k)=DiffSigmaPpEpsGamma(j,k)+DiffSigmaPpDelta(j,k);
        %Total differential stress
            DiffSigmamin(j,k)=DiffSigmaV(j,k)+DiffSigmaSmin(j,k)+DiffSigmaPp(j,k);
            DiffSigmamax(j,k)=DiffSigmaV(j,k)+DiffSigmaSmax(j,k)+DiffSigmaPp(j,k);
            DiffSigmaminratio(j,k)=DiffSigmamin(j,k)/Model.SHMin(j,k);
            DiffSigmamaxratio(j,k)=DiffSigmamax(j,k)/Model.SHMax(j,k);
            DiffRelativeWeightSmin(j,k)=((DiffSigmaSminEpsGamma(j,k)+DiffSigmaPpEpsGamma(j,k))/(DiffSigmaV(j,k)+DiffSigmaSDelta(j,k)+DiffSigmaPpDelta(j,k)));
        %Anisotropic Stresses
            AnisoSHMin(j,k)=DiffSigmamin(j,k)+Model.SHMin(j,k);
            AnisoSHMax(j,k)=DiffSigmamax(j,k)+Model.SHMax(j,k);
            Model.SigmaV(j,k)=Model.SV-Model.Biotv*Model.PPRS;
            Model.SigmaHMin(j,k)=AnisoSHMin(j,k)-Model.Bioth*Model.PPRS;
            Model.SigmaHMax(j,k)=AnisoSHMax(j,k)-Model.Bioth*Model.PPRS;
            if AnisoSHMax(j,k)>Model.SV
                if AnisoSHMin(j,k)>Model.SV
                    AnisoTectRegime(j,k)=3;
                else
                    AnisoTectRegime(j,k)=2;
                end
            else
                AnisoTectRegime(j,k)=1;
            end
    end
end
%Calculation of first non-empty point at bottom
count_x_inf=1;
count_y_inf=1;
while isnan(Model.TStrainmin(count_x_inf,count_y_inf))==1
    count_x_inf=count_x_inf+1;
    if count_x_inf==length(Model.SmaxSVfraction)
        count_y_inf=count_y_inf+1;
        count_x_inf=1;
    end
end
%Calculation of first non-empty point at top
% count_x_top=1;
% while isnan(Model.TStrainmin(length(Model.SmaxSVfraction),count_x_top))==1
%     count_x_top=count_x_top+1;
% end
% hold on
% %Calculation of firsts non-empty points at SV
% minx=abs(Model.SminSVfraction-1);
% limitx=find(minx==min(minx));
% count_x_side=1;
% while isnan(Model.TStrainmin(limitx,count_x_side))==1
%     count_x_side=count_x_side+1;
% end
% miny=abs(Model.SmaxSVfraction-1);
% limity=find(minx==min(minx));
% count_y_side=length(Model.SmaxSVfraction);
% while isnan(Model.TStrainmin(count_y_side,limity))==1
%     count_y_side=count_y_side-1;
% end

figure(1)
% h=imagesc(Model.SminSVfraction*Model.SV,Model.SmaxSVfraction*Model.SV,DiffSigmaminratio*100)
h=imagesc(Model.SminSVfraction,Model.SmaxSVfraction,DiffSigmamaxratio)
set(gca,'Ydir','normal')
set(gca,'Ylim',[min(Model.Sminimum,Model.Sminimum_ani) max(Model.Smaximum,Model.Smaximum_ani)])
set(gca,'Xlim',[min(Model.Sminimum,Model.Sminimum_ani) max(Model.Smaximum,Model.Smaximum_ani)])
colorbar
%-0.02 to 0.18
%-0.1 to 0.3
% caxis([-0.1 0.3]);
colormap jet
% axis image off
if ndims( DiffSigmaminratio ) == 2
  set(h, 'AlphaData', ~isnan(DiffSigmaminratio))
elseif ndims( DiffSigmaminratio ) == 3
  set(h, 'AlphaData', ~isnan(DiffSigmaminratio(:, :, 1)))
end
grid on
hold on

line([Model.Sminimum Model.Smaximum],[Model.Sminimum Model.Smaximum],'LineWidth',2,'Color','black')

line([Model.Sminimum Model.Sminimum],[Model.Sminimum Model.SV],'LineWidth',2,'Color','black')

line([Model.Sminimum Model.SV],[Model.SV Model.Smaximum],'LineWidth',2,'Color','black')

line([Model.SV Model.Smaximum],[Model.Smaximum Model.Smaximum],'LineWidth',2,'Color','black')

line([Model.SV Model.Sminimum],[Model.SV Model.SV],'LineWidth',2,'Color','black','LineStyle','--')

line([Model.SV Model.SV],[Model.SV Model.Smaximum],'LineWidth',2,'Color','black','LineStyle','--')

%Aniso Model

% line([Model.Sminimum_ani Model.Smaximum_ani],[Model.Sminimum_ani Model.Smaximum_ani],'LineWidth',2,'Color','magenta')
% 
% line([Model.Sminimum_ani Model.Sminimum_ani],[Model.Sminimum_ani Model.SV],'LineWidth',2,'Color','magenta')
% 
% line([Model.Sminimum_ani Model.SV],[Model.SV Model.Smaximum_ani],'LineWidth',2,'Color','magenta')
% 
% line([Model.SV Model.Smaximum_ani],[Model.Smaximum_ani Model.Smaximum_ani],'LineWidth',2,'Color','magenta')
% %Points

scatter(Model.SV,Model.SV,50,'black','filled')
hold on
scatter(Model.Case1_Sh,Model.Case1_SH,50,'black','filled')
hold on
scatter(Model.Case2_Sh,Model.Case2_SH,50,'black','filled')
hold on
scatter(Model.Case3_Sh,Model.Case3_SH,50,'black','filled')
hold on
% scatter(Model.Case1_Sh_ani,Model.Case1_SH_ani,50,'magenta','filled')
% hold on
% scatter(Model.Case2_Sh_ani,Model.Case2_SH_ani,50,'magenta','filled')
% hold on
% scatter(Model.Case3_Sh_ani,Model.Case3_SH_ani,50,'magenta','filled')

%Log

% Dataset.YME_V_psi=Dataset.YME_V_psi*1E6;
% Dataset.YME_H_psi=Dataset.YME_H_psi*1E6;

%Data Loading
Dataset.Depth_res=resample(DEPTH,4,1);
Dataset2.Depth=Dataset.Depth_res(173:293);
Dataset.SigV_res=resample(Dataset.SigV_psi,4,1);
Dataset2.SigV_psi=Dataset.SigV_res(173:293)
Dataset.PPRS_res=resample(Dataset.PPRS_psi,4,1);
Dataset2.PPRS_psi=Dataset.PPRS_res(173:293)
Dataset.C11_psi=(1./((1-Dataset.PR_H_psi).*Dataset.YME_V_psi-2.*Dataset.PR_V_psi.^2.*Dataset.YME_H_psi)).*(Dataset.YME_H_psi.*Dataset.YME_V_psi-Dataset.PR_V_psi.^2.*Dataset.YME_H_psi.^2)./(1+Dataset.PR_H_psi);
Dataset.C11_res=resample(Dataset.C11_psi,4,1);
Dataset2.C11_psi=Dataset.C11_res(173:293);
Dataset.C33_psi=(1./((1-Dataset.PR_H_psi).*Dataset.YME_V_psi-2.*Dataset.PR_V_psi.^2.*Dataset.YME_H_psi)).*(Dataset.YME_V_psi.^2-Dataset.PR_H_psi.*Dataset.YME_V_psi.^2);
Dataset.C33_res=resample(Dataset.C33_psi,4,1);
Dataset2.C33_psi=Dataset.C33_res(173:293);
Dataset.C12_psi=(1./((1-Dataset.PR_H_psi).*Dataset.YME_V_psi-2.*Dataset.PR_V_psi.^2.*Dataset.YME_H_psi)).*(Dataset.PR_V_psi.^2.*Dataset.YME_H_psi.^2+Dataset.PR_H_psi.*Dataset.YME_H_psi.*Dataset.YME_V_psi)./(1+Dataset.PR_H_psi);
Dataset.C12_res=resample(Dataset.C12_psi,4,1);
Dataset2.C12_psi=Dataset.C12_res(173:293);
Dataset.C13_psi=(1./((1-Dataset.PR_H_psi).*Dataset.YME_V_psi-2.*Dataset.PR_V_psi.^2.*Dataset.YME_H_psi)).*(Dataset.PR_V_psi.*Dataset.YME_V_psi.*Dataset.YME_H_psi);
Dataset.C13_res=resample(Dataset.C13_psi,4,1);
Dataset2.C13_psi=Dataset.C13_res(173:293);
Dataset.C66_psi=(Dataset.C11_psi-Dataset.C12_psi)./2;
Dataset.C66_res=resample(Dataset.C66_psi,4,1);
Dataset2.C66_psi=Dataset.C66_res(173:293);

% plot(Dataset.C11_psi,DEPTH*25)
% hold on
% plot(Dataset2.C11,Dataset2.Depth*25)
%Biot parameters computation
Dataset.BiotV=1-(2.*Dataset.C13_psi+Dataset.C33_psi)./(3.*76.8E9.*0.00014504);
Dataset2.BiotV=1-(2.*Dataset2.C13_psi+Dataset2.C33_psi)./(3.*76.8E9.*0.00014504);
Dataset.BiotH=1-(Dataset.C11_psi+Dataset.C12_psi+Dataset.C13_psi)./(3.*76.8E9.*0.00014504);
Dataset2.BiotH=1-(Dataset2.C11_psi+Dataset2.C12_psi+Dataset2.C13_psi)./(3.*76.8E9.*0.00014504);

clear errorh errorH strain_h_index strain_H_index

for j=1:length(Dataset2.C33_psi)
    if Dataset2.C33_psi(j)>3.8e6
        clayflag2(j)=0;
    else
        clayflag2(j)=1;
    end
end
%Point 1: Sh=SH=0.8e4
h_1=Model.Case1_TSMin;
H_1=Model.Case1_TSMax;
%Point 2: Sh=0.9e4 SH=1e4
h_2=Model.Case2_TSMin;
H_2=Model.Case2_TSMax;
%Point 3: Sh=0.9e4 SH=1.2e4
h_3=Model.Case3_TSMin;
H_3=Model.Case3_TSMax;
% Dataset.strain_h=0.0002;
% Dataset.strain_H=0.0006;
Dataset.strain_h=h_3;
Dataset.strain_H=H_3;
Dataset.tau=(Dataset.strain_H-Dataset.strain_h)./Dataset.strain_h;
Dataset.SigH_calc=(Dataset.YME_H_psi./Dataset.YME_V_psi).*(Dataset.PR_V_psi./(1-Dataset.PR_H_psi)).*(Dataset.SigV_psi-Dataset.BiotV.*Dataset.PPRS_psi)+Dataset.YME_H_psi./(1-Dataset.PR_H_psi.^2).*(Dataset.strain_H+Dataset.PR_H_psi.*Dataset.strain_h)+Dataset.BiotH.*Dataset.PPRS_psi;
Dataset.Sigh_calc=(Dataset.YME_H_psi./Dataset.YME_V_psi).*(Dataset.PR_V_psi./(1-Dataset.PR_H_psi)).*(Dataset.SigV_psi-Dataset.BiotV.*Dataset.PPRS_psi)+Dataset.YME_H_psi./(1-Dataset.PR_H_psi.^2).*(Dataset.strain_h+Dataset.PR_H_psi.*Dataset.strain_H)+Dataset.BiotH.*Dataset.PPRS_psi;

Dataset.Epsilon=(Dataset.C11_psi-Dataset.C33_psi)./(2*Dataset.C33_psi);
Dataset2.Epsilon=(Dataset2.C11_psi-Dataset2.C33_psi)./(2*Dataset2.C33_psi);
Dataset.Gamma=Dataset.Epsilon;
Dataset2.Gamma=Dataset2.Epsilon;
Dataset.C44_psi=Dataset.C66_psi./(1+2*Dataset.Gamma);
Dataset2.C44_psi=Dataset2.C66_psi./(1+2*Dataset2.Gamma);
Dataset.Delta=((Dataset.C13_psi+Dataset.C44_psi).^2-(Dataset.C33_psi-Dataset.C44_psi).^2)./(2.*Dataset.C33_psi.*(Dataset.C33_psi-Dataset.C44_psi));
Dataset2.Delta=((Dataset2.C13_psi+Dataset2.C44_psi).^2-(Dataset2.C33_psi-Dataset2.C44_psi).^2)./(2.*Dataset2.C33_psi.*(Dataset2.C33_psi-Dataset2.C44_psi));
Dataset.C13_iso=Dataset.C33_psi-2*Dataset.C44_psi;
Dataset2.C13_iso=Dataset2.C33_psi-2*Dataset2.C44_psi;
Dataset.C11_ani=Dataset.C33_psi.*(1+2*Model.Eps.*clayflag);
Dataset2.C11_ani=Dataset2.C33_psi.*(1+2*Model.Eps.*clayflag2);
Dataset.C66_ani=Dataset.C44_psi.*(1+2*Model.Gamma.*clayflag);
Dataset2.C66_ani=Dataset2.C44_psi.*(1+2*Model.Gamma.*clayflag2);
Dataset.C13_ani=-Dataset.C44_psi+sqrt((Dataset.C33_psi-Dataset.C44_psi).^2+2.*Model.Delta.*clayflag.*(Dataset.C33_psi.^2-Dataset.C33_psi.*Dataset.C44_psi));
Dataset2.C13_ani=-Dataset2.C44_psi+sqrt((Dataset2.C33_psi-Dataset2.C44_psi).^2+2.*Model.Delta.*clayflag2.*(Dataset2.C33_psi.^2-Dataset2.C33_psi.*Dataset2.C44_psi));

Dataset.Biotiso=1-(2.*Dataset.C13_iso+Dataset.C33_psi)./(3.*76.8E9.*0.00014504);
Dataset2.Biotiso=1-(2.*Dataset2.C13_iso+Dataset2.C33_psi)./(3.*76.8E9.*0.00014504);
Dataset.Sigh_iso=(Dataset.C13_iso./Dataset.C33_psi).*(Dataset.SigV_psi-Dataset.Biotiso.*Dataset.PPRS_psi)-(Dataset.C13_iso.^2./Dataset.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset.C44_psi.*(Dataset.strain_H)+Dataset.Biotiso.*Dataset.PPRS_psi;
Dataset2.Sigh_iso=(Dataset2.C13_iso./Dataset2.C33_psi).*(Dataset2.SigV_psi-Dataset2.Biotiso.*Dataset2.PPRS_psi)-(Dataset2.C13_iso.^2./Dataset2.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset2.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset2.C44_psi.*(Dataset.strain_H)+Dataset2.Biotiso.*Dataset2.PPRS_psi;
Dataset.Sigh_iso_SigmaV=(Dataset.C13_iso./Dataset.C33_psi).*(Dataset.SigV_psi);
Dataset2.Sigh_iso_SigmaV=(Dataset2.C13_iso./Dataset2.C33_psi).*(Dataset2.SigV_psi);
Dataset.Sigh_iso_Pp=(Dataset.C13_iso./Dataset.C33_psi).*(-Dataset.Biotiso.*Dataset.PPRS_psi)+Dataset.Biotiso.*Dataset.PPRS_psi;
Dataset2.Sigh_iso_Pp=(Dataset2.C13_iso./Dataset2.C33_psi).*(-Dataset2.Biotiso.*Dataset2.PPRS_psi)+Dataset2.Biotiso.*Dataset2.PPRS_psi;
Dataset.Sigh_iso_S=-(Dataset.C13_iso.^2./Dataset.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset.C44_psi.*(Dataset.strain_H);
Dataset2.Sigh_iso_S=-(Dataset2.C13_iso.^2./Dataset2.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset2.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset2.C44_psi.*(Dataset.strain_H);
Dataset.SigH_iso=(Dataset.C13_iso./Dataset.C33_psi).*(Dataset.SigV_psi-Dataset.Biotiso.*Dataset.PPRS_psi)-(Dataset.C13_iso.^2./Dataset.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset.C44_psi.*(Dataset.strain_h)+Dataset.Biotiso.*Dataset.PPRS_psi;
Dataset2.SigH_iso=(Dataset2.C13_iso./Dataset2.C33_psi).*(Dataset2.SigV_psi-Dataset2.Biotiso.*Dataset2.PPRS_psi)-(Dataset2.C13_iso.^2./Dataset2.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset2.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset2.C44_psi.*(Dataset.strain_h)+Dataset2.Biotiso.*Dataset2.PPRS_psi;
Dataset.SigH_iso_S=-(Dataset.C13_iso.^2./Dataset.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset.C44_psi.*(Dataset.strain_h);
Dataset2.SigH_iso_S=-(Dataset2.C13_iso.^2./Dataset2.C33_psi).*(Dataset.strain_h+Dataset.strain_H)+Dataset2.C33_psi.*(Dataset.strain_h+Dataset.strain_H)-2.*Dataset2.C44_psi.*(Dataset.strain_h);

Dataset.DiffSigmaV=-(Dataset.C13_iso-Dataset.C13_ani)./Dataset.C33_psi.*Dataset.SigV_psi;
Dataset2.DiffSigmaV=-(Dataset2.C13_iso-Dataset2.C13_ani)./Dataset2.C33_psi.*Dataset2.SigV_psi;
Dataset.DiffSigmaSmin=Dataset.strain_H.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi-4.*Model.Gamma.*clayflag.*Dataset.C44_psi)+Dataset.strain_h.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset.C13_iso-Dataset.C13_ani)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_ani);
Dataset2.DiffSigmaSmin=Dataset.strain_H.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi-4.*Model.Gamma.*clayflag2.*Dataset2.C44_psi)+Dataset.strain_h.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset2.C13_iso-Dataset2.C13_ani)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_ani);
Dataset.DiffSigmaSmax=Dataset.strain_h.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi-4.*Model.Gamma.*clayflag.*Dataset.C44_psi)+Dataset.strain_H.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset.C13_iso-Dataset.C13_ani)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_ani);
Dataset2.DiffSigmaSmax=Dataset.strain_h.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi-4.*Model.Gamma.*clayflag2.*Dataset2.C44_psi)+Dataset.strain_H.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset2.C13_iso-Dataset2.C13_ani)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_ani);
Dataset.DiffSigmaPp=4.*Dataset.PPRS_psi./(3*Model.Ks).*(Model.Gamma.*clayflag.*Dataset.C44_psi-Model.Eps.*clayflag.*Dataset.C33_psi)+Dataset.PPRS_psi.*((Dataset.C13_iso-Dataset.C13_ani)./Dataset.C33_psi+2./3.*1./Model.Ks.*(-Dataset.C13_iso+Dataset.C13_ani)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_ani));
Dataset2.DiffSigmaPp=4.*Dataset2.PPRS_psi./(3*Model.Ks).*(Model.Gamma.*clayflag2.*Dataset2.C44_psi-Model.Eps.*clayflag2.*Dataset2.C33_psi)+Dataset2.PPRS_psi.*((Dataset2.C13_iso-Dataset2.C13_ani)./Dataset2.C33_psi+2./3.*1./Model.Ks.*(-Dataset2.C13_iso+Dataset2.C13_ani)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_ani));
Dataset.DiffSigmamin=Dataset.DiffSigmaV+Dataset.DiffSigmaSmin+Dataset.DiffSigmaPp;
Dataset2.DiffSigmamin=Dataset2.DiffSigmaV+Dataset2.DiffSigmaSmin+Dataset2.DiffSigmaPp;
Dataset.DiffSigmamax=Dataset.DiffSigmaV+Dataset.DiffSigmaSmax+Dataset.DiffSigmaPp;
Dataset2.DiffSigmamax=Dataset2.DiffSigmaV+Dataset2.DiffSigmaSmax+Dataset2.DiffSigmaPp;

Dataset.DiffSigmaV_ane=-(Dataset.C13_iso-Dataset.C13_iso)./Dataset.C33_psi.*Dataset.SigV_psi;
Dataset2.DiffSigmaV_ane=-(Dataset2.C13_iso-Dataset2.C13_iso)./Dataset2.C33_psi.*Dataset2.SigV_psi;
Dataset.DiffSigmaSmin_ane=Dataset.strain_H.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi-4.*Model.Gamma.*clayflag.*Dataset.C44_psi)+Dataset.strain_h.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset.C13_iso-Dataset.C13_iso)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_iso);
Dataset2.DiffSigmaSmin_ane=Dataset.strain_H.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi-4.*Model.Gamma.*clayflag2.*Dataset2.C44_psi)+Dataset.strain_h.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset2.C13_iso-Dataset2.C13_iso)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_iso);
Dataset.DiffSigmaSmax_ane=Dataset.strain_h.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi-4.*Model.Gamma.*clayflag.*Dataset.C44_psi)+Dataset.strain_H.*(2.*Model.Eps.*clayflag.*Dataset.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset.C13_iso-Dataset.C13_iso)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_iso);
Dataset2.DiffSigmaSmax_ane=Dataset.strain_h.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi-4.*Model.Gamma.*clayflag2.*Dataset2.C44_psi)+Dataset.strain_H.*(2.*Model.Eps.*clayflag2.*Dataset2.C33_psi)+(Dataset.strain_H+Dataset.strain_h).*(Dataset2.C13_iso-Dataset2.C13_iso)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_iso);
Dataset.DiffSigmaPp_ane=4.*Dataset.PPRS_psi./(3*Model.Ks).*(Model.Gamma.*clayflag.*Dataset.C44_psi-Model.Eps.*clayflag.*Dataset.C33_psi)+Dataset.PPRS_psi.*((Dataset.C13_iso-Dataset.C13_iso)./Dataset.C33_psi+2./3.*1./Model.Ks.*(-Dataset.C13_iso+Dataset.C13_iso)./Dataset.C33_psi.*(Dataset.C13_iso+Dataset.C13_iso));
Dataset2.DiffSigmaPp_ane=4.*Dataset2.PPRS_psi./(3*Model.Ks).*(Model.Gamma.*clayflag2.*Dataset2.C44_psi-Model.Eps.*clayflag2.*Dataset2.C33_psi)+Dataset2.PPRS_psi.*((Dataset2.C13_iso-Dataset2.C13_iso)./Dataset2.C33_psi+2./3.*1./Model.Ks.*(-Dataset2.C13_iso+Dataset2.C13_iso)./Dataset2.C33_psi.*(Dataset2.C13_iso+Dataset2.C13_iso));
Dataset.DiffSigmamin_ane=Dataset.DiffSigmaV_ane+Dataset.DiffSigmaSmin_ane+Dataset.DiffSigmaPp_ane;
Dataset2.DiffSigmamin_ane=Dataset2.DiffSigmaV_ane+Dataset2.DiffSigmaSmin_ane+Dataset2.DiffSigmaPp_ane;
Dataset.DiffSigmamax_ane=Dataset.DiffSigmaV_ane+Dataset.DiffSigmaSmax_ane+Dataset.DiffSigmaPp_ane;
Dataset2.DiffSigmamax_ane=Dataset2.DiffSigmaV_ane+Dataset2.DiffSigmaSmax_ane+Dataset2.DiffSigmaPp_ane;

Dataset.Sigh_ani=Dataset.Sigh_iso+Dataset.DiffSigmamin;
Dataset2.Sigh_ani=Dataset2.Sigh_iso+Dataset2.DiffSigmamin;
Dataset.Sigh_ane=Dataset.Sigh_iso+Dataset.DiffSigmamin_ane;
Dataset2.Sigh_ane=Dataset2.Sigh_iso+Dataset2.DiffSigmamin_ane;
Dataset.Sigh_ratio=Dataset.DiffSigmamin./Dataset.Sigh_iso.*100;
Dataset2.Sigh_ratio=Dataset2.DiffSigmamin./Dataset2.Sigh_iso.*100;
Dataset.SigH_ani=Dataset.SigH_iso+Dataset.DiffSigmamax;
Dataset2.SigH_ani=Dataset2.SigH_iso+Dataset2.DiffSigmamax;
Dataset.SigH_ane=Dataset.SigH_iso+Dataset.DiffSigmamax_ane;
Dataset2.SigH_ane=Dataset2.SigH_iso+Dataset2.DiffSigmamax_ane;
Dataset.SigH_ratio=Dataset.DiffSigmamax./Dataset.SigH_iso.*100;
Dataset2.SigH_ratio=Dataset2.DiffSigmamax./Dataset2.SigH_iso.*100;

%Figure 2
figure('Color','white')
subplot(1,3,1)
plot(Dataset2.C33_psi,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.C44_psi,Dataset2.Depth*25+2660,'r','LineWidth',2)
hold on
plot(Dataset2.C13_iso,Dataset2.Depth*25+2660,':k','LineWidth',2)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Cij (psi)')
ylabel('Depth (m)')

subplot(1,3,2)
plot(Dataset2.C33_psi,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.C11_ani,Dataset2.Depth*25+2660,'m','LineWidth',2)
hold on
plot(Dataset2.C44_psi,Dataset2.Depth*25+2660,'r','LineWidth',2)
hold on
plot(Dataset2.C66_ani,Dataset2.Depth*25+2665,'Color',[0.58 0.71 0.61],'LineWidth',2)
hold on
plot(Dataset2.C13_ani,Dataset2.Depth*25+2665,'k','LineWidth',2)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Cij (psi)')
ylabel('Depth (m)')

subplot(1,3,3)
plot(Dataset2.C33_psi,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.C11_ani,Dataset2.Depth*25+2660,'m','LineWidth',2)
hold on
plot(Dataset2.C44_psi,Dataset2.Depth*25+2660,'r','LineWidth',2)
hold on
plot(Dataset2.C66_ani,Dataset2.Depth*25+2660,'Color',[0.58 0.71 0.61],'LineWidth',2)
hold on
plot(Dataset2.C13_iso,Dataset2.Depth*25+2660,'k','LineWidth',2)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Cij (psi)')
ylabel('Depth (m)')

%Figures 3, 5, 7
figure('Color','white')
subplot(1,3,1)
plot(Dataset2.Sigh_iso,Dataset2.Depth*25+2660,'k','LineWidth',2)
hold on
plot(Dataset2.SigH_iso,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.SigV_psi,Dataset2.Depth*25+2660,'r','LineWidth',1)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Stress (psi)')
ylabel('Depth (m)')

subplot(1,3,2)
plot(Dataset2.Sigh_ani,Dataset2.Depth*25+2660,'k','LineWidth',2)
hold on
plot(Dataset2.SigH_ani,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.SigV_psi,Dataset2.Depth*25+2660,'r','LineWidth',1)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Stress (psi)')
ylabel('Depth (m)')

subplot(1,3,3)
plot(Dataset2.Sigh_ane,Dataset2.Depth*25+2660,'k','LineWidth',2)
hold on
plot(Dataset2.SigH_ane,Dataset2.Depth*25+2660,'b','LineWidth',2)
hold on
plot(Dataset2.SigV_psi,Dataset2.Depth*25+2660,'r','LineWidth',1)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Stress (psi)')
ylabel('Depth (m)')

%Figures 4,6,8
figure('Color','white')
subplot(1,2,1)
plot(Dataset2.DiffSigmaV+Dataset2.DiffSigmaPp,Dataset2.Depth*25+2660,'r','LineWidth',2)
hold on
plot(Dataset2.DiffSigmaSmin,Dataset2.Depth*25+2660,'k','LineWidth',2)
hold on
plot(Dataset2.DiffSigmaSmax,Dataset2.Depth*25+2660,'b','LineWidth',2)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Stress (psi)')
ylabel('Depth (m)')

subplot(1,2,2)
plot(Dataset2.DiffSigmaV_ane+Dataset2.DiffSigmaPp_ane,Dataset2.Depth*25+2660,'r','LineWidth',2)
hold on
plot(Dataset2.DiffSigmaSmin_ane,Dataset2.Depth*25+2660,'k','LineWidth',2)
hold on
plot(Dataset2.DiffSigmaSmax_ane,Dataset2.Depth*25+2660,'b','LineWidth',2)
set(gca,'Ydir','reverse')
set(gca,'Ylim',[2735 2810])
grid on
xlabel('Stress (psi)')
ylabel('Depth (m)')

%Normalization to SigV
Dataset2.Sigh_iso_norm=Dataset2.Sigh_iso./Dataset2.SigV_psi;
Dataset2.SigH_iso_norm=Dataset2.SigH_iso./Dataset2.SigV_psi;
Dataset2.Sigh_ani_norm=Dataset2.Sigh_ani./Dataset2.SigV_psi;
Dataset2.SigH_ani_norm=Dataset2.SigH_ani./Dataset2.SigV_psi;
Dataset2.Sigh_ane_norm=Dataset2.Sigh_ane./Dataset2.SigV_psi;
Dataset2.SigH_ane_norm=Dataset2.SigH_ane./Dataset2.SigV_psi;

Model.Case1_Sh_norm=Model.Case1_Sh/Model.SV;
Model.Case1_SH_norm=Model.Case1_SH/Model.SV;
Model.Case2_Sh_norm=Model.Case2_Sh/Model.SV;
Model.Case2_SH_norm=Model.Case2_SH/Model.SV;
Model.Case3_Sh_norm=Model.Case3_Sh/Model.SV;
Model.Case3_SH_norm=Model.Case3_SH/Model.SV;

Model.Sminimum_norm=Model.Sminimum/Model.SV;
Model.Sminimum_ani_norm=Model.Sminimum_ani/Model.SV;
Model.Smaximum_norm=Model.Smaximum/Model.SV;
Model.Smaximum_ani_norm=Model.Smaximum_ani/Model.SV;

Model.SmaxSVfraction_norm=linspace(Model.Sminimum/Model.SV,Model.Smaximum/Model.SV,300);
Model.SminSVfraction_norm=linspace(Model.Sminimum/Model.SV,Model.Smaximum/Model.SV,300);

figure(123)
k=imagesc(Model.SminSVfraction_norm,Model.SmaxSVfraction_norm,DiffSigmamaxratio)
set(gca,'Ydir','normal')
set(gca,'Ylim',[0.6 1.9])
set(gca,'Xlim',[0.6 1.8])
colorbar
%-0.02 to 0.18
%-0.1 to 0.3
% caxis([-0.1 0.3]);
%Calibration points
if ndims( DiffSigmaminratio ) == 2
  set(k, 'AlphaData', ~isnan(DiffSigmaminratio))
elseif ndims( DiffSigmaminratio ) == 3
  set(k, 'AlphaData', ~isnan(DiffSigmaminratio(:, :, 1)))
end
grid on
hold on
% scatter(Model.Case1_Sh_norm,Model.Case1_SH_norm,50,'black','filled')
% hold on
% scatter(Model.Case2_Sh_norm,Model.Case2_SH_norm,50,'black','filled')
% hold on
% scatter(Model.Case3_Sh_norm,Model.Case3_SH_norm,50,'black','filled')
% Isotropic models
scatter(Dataset2.Sigh_iso_norm_Case3,Dataset2.SigH_iso_norm_Case3,10,'black','filled')
hold on
scatter(Dataset2.Sigh_iso_norm_Case2,Dataset2.SigH_iso_norm_Case2,10,'black','filled')
hold on
scatter(Dataset2.Sigh_iso_norm_Case1,Dataset2.SigH_iso_norm_Case1,10,'black','filled')
%Anisotropic models
scatter(Dataset2.Sigh_ani_norm_Case3,Dataset2.SigH_ani_norm_Case3,10,'red','filled')
hold on
scatter(Dataset2.Sigh_ani_norm_Case2,Dataset2.SigH_ani_norm_Case2,10,'red','filled')
hold on
scatter(Dataset2.Sigh_ani_norm_Case1,Dataset2.SigH_ani_norm_Case1,10,'red','filled')
% Limits
line([1 Model.Sminimum_ani_norm],[1 1],'LineWidth',2,'Color','red','LineStyle','--')
line([1 1],[1 Model.Smaximum_ani_norm],'LineWidth',2,'Color','red','LineStyle','--')
line([1 Model.Sminimum_norm],[1 1],'LineWidth',2,'Color','black','LineStyle','--')
line([1 1],[1 Model.Smaximum_norm],'LineWidth',2,'Color','black','LineStyle','--')

line([Model.Sminimum_ani_norm Model.Smaximum_ani_norm],[Model.Sminimum_ani_norm Model.Smaximum_ani_norm],'LineWidth',2,'Color','red')
line([Model.Sminimum_ani_norm Model.Sminimum_ani_norm],[Model.Sminimum_ani_norm 1],'LineWidth',2,'Color','red')
line([Model.Sminimum_ani_norm 1],[1 Model.Smaximum_ani_norm],'LineWidth',2,'Color','red')
line([1 Model.Smaximum_ani_norm],[Model.Smaximum_ani_norm Model.Smaximum_ani_norm],'LineWidth',2,'Color','red')

line([Model.Sminimum_norm Model.Smaximum_norm],[Model.Sminimum_norm Model.Smaximum_norm],'LineWidth',2,'Color','black')
line([Model.Sminimum_norm Model.Sminimum_norm],[Model.Sminimum_norm 1],'LineWidth',2,'Color','black')
line([Model.Sminimum_norm 1],[1 Model.Smaximum_norm],'LineWidth',2,'Color','black')
line([1 Model.Smaximum_norm],[Model.Smaximum_norm Model.Smaximum_norm],'LineWidth',2,'Color','black')

% figure
% scatter(Model.Case1_Sh,Model.Case1_SH,50,'black','filled')
% hold on
% scatter(Model.Case2_Sh,Model.Case2_SH,50,'black','filled')
% hold on
% scatter(Model.Case3_Sh,Model.Case3_SH,50,'black','filled')
% % scatter(Dataset.Sigh_iso./Dataset.SigV_psi,Dataset.SigH_iso./Dataset.SigV_psi,10,Dataset.C33_psi)
% % hold on
% % scatter(Dataset.Sigh_ani./Dataset.SigV_psi,Dataset.SigH_ani./Dataset.SigV_psi,10,Dataset.C33_psi,'filled')
% set(gca,'Ydir','normal')
% set(gca,'Ylim',[min(Model.Sminimum,Model.Sminimum_ani) max(Model.Smaximum,Model.Smaximum_ani)])
% set(gca,'Xlim',[min(Model.Sminimum,Model.Sminimum_ani) max(Model.Smaximum,Model.Smaximum_ani)])
% grid on
% 
% line([Model.Sminimum Model.Smaximum],[Model.Sminimum Model.Smaximum],'LineWidth',2,'Color','black')
% 
% line([Model.Sminimum Model.Sminimum],[Model.Sminimum Model.SV],'LineWidth',2,'Color','black')
% 
% line([Model.Sminimum Model.SV],[Model.SV Model.Smaximum],'LineWidth',2,'Color','black')
% 
% line([Model.SV Model.Smaximum],[Model.Smaximum Model.Smaximum],'LineWidth',2,'Color','black')
% 
% line([Model.SV Model.Sminimum],[Model.SV Model.SV],'LineWidth',2,'Color','black','LineStyle','--')
% 
% line([Model.SV Model.SV],[Model.SV Model.Smaximum],'LineWidth',2,'Color','black','LineStyle','--')
% 
% 
% %Aniso Model
% 
% % line([Model.Sminimum_ani/Model.SV Model.Smaximum_ani/Model.SV],[Model.Sminimum_ani/Model.SV Model.Smaximum_ani/Model.SV],'LineWidth',2,'Color','magenta')
% % 
% % line([Model.Sminimum_ani Model.Sminimum_ani],[Model.Sminimum_ani Model.SV],'LineWidth',2,'Color','magenta')
% % 
% % line([Model.Sminimum_ani Model.SV],[Model.SV Model.Smaximum_ani],'LineWidth',2,'Color','magenta')
% % 
% % line([Model.SV Model.Smaximum_ani],[Model.Smaximum_ani Model.Smaximum_ani],'LineWidth',2,'Color','magenta')
"""
