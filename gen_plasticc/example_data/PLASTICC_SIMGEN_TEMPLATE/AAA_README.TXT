   PLASTICC: General Information about SNANA Simulations

# =============================================
#     GENERATION INSTRUCTIONS on MIDWAY
# =============================================

cd $PLASTICC_ROOT/SIMGEN

# create SIMSED binaries
# Check MAKE*.LOG files in $PLASTICC_MODELS/SIMSED_BINARIES
./MAKE_SIMSED_BINARIES  

# construct DDF and WDF SIMGEN-MASTER inputs from template-input
./MAKE_SIMGEN_MASTER

# launch IDEAL and LSST jobs
sim_SNmix.pl SIMGEN_MASTER_IDEAL_z02.INPUT NOPROMPT >& DMP_SIMGEN_IDEAL_z02.LOG &
sim_SNmix.pl SIMGEN_MASTER_LSST_DDF.INPUT  NOPROMPT >& DMP_SIMGEN_LSST_DDF.LOG &
sim_SNmix.pl SIMGEN_MASTER_LSST_WFD.INPUT  NOPROMPT >& DMP_SIMGEN_LSST_WFD.LOG &

# obsolete jobs:
sim_SNmix.pl SIMGEN_MASTER_IDEAL_zALL.INPUT NOPROMPT >& DMP_SIMGEN_IDEAL_zALL.LOG &
sim_SNmix.pl SIMGEN_MASTER_SDSS.INPUT      NOPROMPT >& DMP_SIMGEN_SDSS.LOG &

mv $SNDATA_ROOT/SIM/*MODEL*  $LSST_SIM
cd $LSST_SIM ;  $PLASTICC_ROOT/SIMGEN/MAKE_TARFILES
# archive SIMLOGS_XXX under SIMLOGS_Archive
# append this file with TOTALs

# =============================================
#          SAMPLES
# =============================================
  LSST_DDF  : LSST deep drill (5 pointings,        59580<MJD<63223.1
  LSST_WFD  : LSST wide-fast-deep (~18,000 sqdeg,  59580<MJD<63229.4)
  SDSS      : stripe 82
  IDEAL     : LSST bands, x1000 exposure time, 300 days, 2 day cadence
  IDEAL_z02 : z=0.02, LSST bands, x1000 exposure time, 300 days, 2 day cadence

# ===============================================================
#    MODEL LIST  (May 9 2018: beware renumbering for CC-II/Ibc)
# ===============================================================


MODEL02   CC-II              (II  templates, Jones 2017)
MODEL03   CC-Ibc             (Ibc templates, Jones 2017)
MODEL11   SNIa               (normal, for cosmology measurements)
MODEL12   IIpca              (from Santiago & Lluis)
MODEL13   MOSFIT_Ibc
MODEL14   MOSFIT_IIn
MODEL41   SNIa-91bg         (newer model from Santiago)
MODEL42   SNIa-91bg         (older model from Jones 2017 with 4 templates)
MODEL43   SNIax             (peculiar Ia sub-type)
MODEL45  *pointIa
MODEL50   Kilonova-GW170817 (single event)
MODEL51   Kilonova-Kasen    (330 models over VK,MASS,XLAN)
MODEL60   MOSFIT_SLSN_MAGNETAR
MODEL61  *MOSFIT_PISN          (Pair-Instability)
MODEL62  *MOSFIT_ILOT          (Intermediate Luminosity Optical Transients)
MODEL63  *MOSFIT_CART          (CAlcium-Rich Transients)
MODEL64  *MOSFIT_TDE           (Tidal Disruption Event)
MODEL70   AGN                  (from LSST model)
MODEL80   RRLyrae
MODEL81   Mdwarf_flares
MODEL83   PHOEBE               (eclipsing binaries from Andrej Prsa)
MODEL84   [Mira]
MODEL90  *uLens_CFA_BinarySource  (Binary Source, CFA)
MODEL91   uLens_GaiaStar          (single-source, Bachelet)
MODEL92  *uLens_STRING            (cosmic string model)
MODEL93   uLens_CFA_SingleSource  (Single Source, CFA)

*  --> never observed, or too few events for training set
[] --> model devel in progress, not yet available



# =============================================
#           ZEROPOINTS
# =============================================

The FLUXCAL and FLUXCAL_ERR are calibrated fluxes with a SNANA
zeropoint of ZP_SNANA = 27.5. ZP_SNANA applies to simulations
and data.  The first DDF event in MODEL01 (59825.262, r band)
has SIM_MAGOBS = 23.8065, so the true FLUXCAL  is
    FLUXCAL(true) = 10^[0.4*(27.5-23.8065)] = 30.02
which can be compared to the measured FLUXCAL = 28.76167 +- 0.9550397.

There is a ZEROPT column as well, but this is the observed
zero point for the exposure, in ADU. This ZEROPT would be
used to calibrate the image with a set of standard stars,
and ZEROPT also indicates the relative transmission of the
atmosphere+telescope.

The ZEROPT information is probably not useful for the challenge,
but it is useful to analyze real data. The set of columns,
{ZEROPT,SKY_SIG,PSF,GAIN}, along with the surface brightness
in the HEAD file, can be used to compute the noise.
This is useful to analyze fakes overlaid on images, where the
calculated error can be compared to the photometry-pipeline
error, and differences can turned into corrections.


# =============================================
#              ISSUES 
# =============================================

 [+ means done or fixed, - means not done]

+ spec-z fracion vs. redshift

+ DDF SIMLIB still has just 1 pointing per field; need updated
  SIMLIB with same sky density as WFD.
- have dN/db  for RRlyra, EBE, uLens, but need flatter
   distribution for Mdwarf (Rafael).
- Need absolute numbers to generate for Galactic models.

# ===================================================
     May 11 2018, SNANA v10_60i

  OVERVIEW:
    The main "BEWARE" issue is that the CC model-numbers have
    changed: see "MODEL LIST" above.
    
    After the NYU meeting, I started implementing the easiest tasks
    first with the goal of another data sample over the weekend.
    Maybe one more generation next week will be good enough for
    a first submission to Kaggle ? Updates include: new models,
    realistic CC rate, reasonable-size training set, photo-z,
    extrapolate late-time light-curve mags, sauration cuts.
    
    In addition to adding a few new models (AGN,Iax,EBE), the two
    CC models are now generated with half the rate each, so that
    the combined set of CC models corresponds to one CC sample.
    This change allows us to get a better sense of the data size,
    and the size of the newly-tagged "spectroscopic training" set
    with pre-scales designed to have a few thousand training events.

    To avoid confusion with modified model numbers, the previous
    AAA_README and previous data sets have been stuffed into an
    Archive directory.

    To help prepare for the data release, the statistics summary
    now includes NSPEC, the number of events in the training sample,
    and a global statistics SUM over models. Some quick SUM-numbers:
    107 million transient events were generated, 2.6 million passed
    trigger and were written to data files,, and 3300 were tagged as
    a spectroscopic training set. The Galactic numbers are probably
    way too low, so the 2.6 million number could get larger in later
    generations.
    
    Details of the changes are given below.
    
  MODEL UPDATES:
     * 91bg update from Santiago; includes Y-band. Using real 91bg
       events, they find that dispersion decreases in redder bands,
       so recommendation is NOT to add artificial dispersion.
       Removed older 91bg MODEL42 that was based on 4 templates.
     * PointIa: followig Saurabh's suggestion, remove brightest
       template, and reduce dispersion from 0.6 to 0.4 mag.
     * Added new LSST-AGN (MODEL82) from Scott Daniel.
     * Added Eclipsing binary (MODEL83) from Adjrs Pras;
         only 1 light curve template here.
     * Added Iax (MODEL43) from Saurabh
     * Hybrid CC-II  model: 50% from ancient templates, 50% from IIpca
     * Hybrid CC-Ibc model: 50% from ancient templates, 50% from MOSFIT-Ibc
     * BEWARE: CC MODEL02 is now split into MODEL02(II) and MODEL03(Ibc)
     
  CODE UPDATES:
     * for T > Tmax(model), use linear-mag extrapolation
       to avoid sharp cutoff artifact.
     * require at least 10 unsaturated obs per band in grizY.
       Don't require u-band because some DDFs don't have enough obs.
         --> uLens_BSR (MODEL90) has only 3% eff for this new cut;
	     Rosanne responsed that she can update the model next week.
     * scale DES spectroscopic efficiency for training set. 
        DDF Scale=0.5   for SNIa; Scale=1 for other models.
        WFD Scale=0.002 for SNIa; Scale=0.004 for other models
       [did not yet make Spec-efficiency shift as discussed at NYU]

   PHOTO-Z UPDATE:
    * Following the NYU discussion, host Photo-z error model is
      0.02*(1+z) with 10% flat-outlier distribution from 0.01 to 3.5.
      I don't have access to a library with Sersic profiles,
      so host Poisson noise is NOT modeled.
      HEADER-FITS columns:  HOSTGAL_PHOTOZ and HOSTGAL_PHOTOZ_ERR
      

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  41150     14013  (725) 
LSST_DDF_MODEL02                  69760      4516  (122) 
LSST_DDF_MODEL03                  29900      2523  (139) 
LSST_DDF_MODEL12                  69760      5533  (18) 
LSST_DDF_MODEL13                  29900      1224  (74) 
LSST_DDF_MODEL14                  17030       531  (38) 
LSST_DDF_MODEL41                   3510       423  (46) 
LSST_DDF_MODEL43                  22910       866  (50) 
LSST_DDF_MODEL45                    290         3  (0) 
LSST_DDF_MODEL50                     20         0  (0) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    250       149  (41) 
LSST_DDF_MODEL61                     20         8  (0) 
LSST_DDF_MODEL62                  11960        21  (0) 
LSST_DDF_MODEL63                   7490        60  (2) 
LSST_DDF_MODEL64                    150        98  (17) 
LSST_DDF_MODEL80                    150        10  (10) 
LSST_DDF_MODEL81                    100        59  (56) 
LSST_DDF_MODEL82                    150       150  (98) 
LSST_DDF_MODEL83                    150       150  (149) 
LSST_DDF_MODEL90                     20         0  (0) 
LSST_DDF_MODEL91                    100         0  (0) 
# -------------------------------------------------------------
SUM-DDF                           304790     30338  (1585) 



#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               14420000   1494610  (733) 
LSST_WFD_MODEL02               24440000    316229  (148) 
LSST_WFD_MODEL03               10470000    180665  (145) 
LSST_WFD_MODEL12               24440000    196783  (44) 
LSST_WFD_MODEL13               10470000     95643  (70) 
LSST_WFD_MODEL14                5967000     46132  (39) 
LSST_WFD_MODEL41                1232000     36287  (47) 
LSST_WFD_MODEL43                8025000     56702  (46) 
LSST_WFD_MODEL45                 104080       209  (0) 
LSST_WFD_MODEL50                   6640        20  (1) 
LSST_WFD_MODEL51                   6640        39  (0) 
LSST_WFD_MODEL60                  89040     34096  (51) 
LSST_WFD_MODEL61                   5240      1091  (2) 
LSST_WFD_MODEL62                4190000      1465  (2) 
LSST_WFD_MODEL63                2626000      2856  (4) 
LSST_WFD_MODEL64                  54240     22753  (23) 
LSST_WFD_MODEL80                 150000     48411  (192) 
LSST_WFD_MODEL81                 100000     14260  (57) 
LSST_WFD_MODEL82                 100000     72013  (66) 
LSST_WFD_MODEL83                  10000      9667  (50) 
LSST_WFD_MODEL90                    280         0  (0) 
LSST_WFD_MODEL91                  30000         0  (0) 
# -------------------------------------------------------------
SUM-WFD                        106936160   2629931  (1720) 


# ===================================================
        June 03 2018, SNANA v10_60c
    
  TRANSIENT MODEL UPDATES:
    + SLSN_MAGNETAR
      To avoid going past z>3.5 where photo-z libary is not defined,
      remove ~30 of the brightest models giving WFD triggers and
      z>3.5 & i_peak<23. Also truncate zMax < 3.45.

    + AGN: select REDSHIFT < 3.5 to associate with photo-z library.
    
    + MOSFIT_TDE: update from Ashley [removed 4 long-duration events]

    + MOSFIT_CART: update from Ashley [0.5 day bins fixes rise-time artifact]
    
    + NON1ASED-II/Ibc
      Switch to Peirels & Rodney templates with NIR extension to
      avoid Y-band drop out at low redshift (paper will be out well
      before PLASTICC ends).

    + NON1ASED-II: Add 7 of P.Brown's AggieNova templates
      (NON1A_INDEX=270-276). However, three of them (270,273,275)
      are way brighter than SNIa, so removed these 3 (leaving 4).
      Waiting for P.Brown to investigate.

    + AGN: redshift converted into photo-z with sigma = 0.05*(1+ztrue).
      Sim structure for this model doesn't allow using photo-z library,
      so will have to use analytical photo-z hack for AGN.
      BEWARE AGN artifact: same redshift used several times in library.
      
  SIMULATION UPDATES
    + zSpec and zPhot udpates ... see below.
    + add lensing. I thought this was in from the start, but it wasn't.
      This feature adds asymmetric mag scatter, with RMS ~ 0.055*z.
      Lensing model based on MICE simulation.
      See LENSDMU in SIMGEN-DUMP file.
    + increase spec-efficiency depth (from DES) by 0.2 mag.
    + Extrapolate UV fluxes down to 500 A to eliminate missing-band
      artifacts in the u & g bands. Extrapolates SED flux linearly
      from Flux(minLam) to Flux(500)=0, where minLam is the minimum
      wavelength defined in the SED model. The extrapolation is
      done in each DAY bin.
    + remove "other" from training sample for never-observed transients.
      These include PISN, pointIa, uLens(BSR), uLens(string).
    + adjust WFD spectroscopic (training set) pre-scales for rare
      events, to ensure at least a few dozen per class.
      Will probably need one more adjustment after this data version.
    + require best redshift (spec or photo-z) < 3 to stay well away
      from edge of photo-z library.

    + There are now three general categories of events flagged by
      SIM_SEARCHEFF_MASK column:
         SIM_SEARCHEFF_MASK = 1 --> pass 2 detection trigger
  	                             [unclassified with host photo-z]
         SIM_SEARCHEFF_MASK = 3 --> pass 2-detect trigger and spec-classified
	                              with spec-z
	 SIM_SEARCHEFF_MASK = 5 --> pass 2 detection trigger + zHOST(spec)
	                             [unclassified]
	 
      Note that SIM_SEARCHEFF_MASK is a bit mask where:
          bit0 -> pass 2 detection trigger
	  bit1 -> spectroscopic classified
	  bit2 -> unclassifed, but zHOST(spec)
	  
  REBINNING:
    + with models getting bigger, the following models were re-binned
      at late times:  SLSN_MAGNETAR, TDE, CART
      
  REDSHIFT UPDATES:
    Still using analytical photo-z model while waiting for Graham updates
    based on her paper (Fig 5 in 1706.09507). Reduced catastrophic outlier
    fraction to 2% (was 10% last data version).

    For Galactic models, all redshifts and errors are zero by default
    (before they were -9)
    
    Setup zHOST file to specify EFF(zspecHOST) vs. zTRUE, corresponding
    to existing redshift catalogs. Function is loosely based on 
    1710.04223 for z<0.1, and uses 4MOST efficiency predictions from
    Jeff Newman. See assoicated file SEARCHEFF_zHOST_PLASTICC.DAT .
    Large number of spec-z in WFD (~0.7 million) could be a
    mis-interpretation, so let's focus on spec-z efficiency model
    for next round.
    Note that spec-confirmed sample has accurate spec-z, and thus
    EFF(zspecHOST) applies to unconfirmed only.
    Redshift data columns to include in challenge are

       HOSTGAL_PHOTOZ +- HOSTGAL_PHOTOZ_ERR
       HOSTGAL_SPECZ  +- HOSTGAL_SPECZ_ERR
       
    For unclassified events with no zHOST, HOSTGAL_SPECZ = -9 +_ -9,
    so maybe convert to NULLL or NaN for Kaggle.

    Check on number of spectroscopic redshifts:
                                 DDF  WFD
         SPEC-CLASSIFIED:       1517  
	 zHOST(unclassified):   4432
	 ---------------------------------------
	 TOTAL  zSpec           5949
	 

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               14420000   1498486  (930) 
LSST_WFD_MODEL02               24440000    394613  (306) 
LSST_WFD_MODEL03               10470000     64629  (67) 
LSST_WFD_MODEL12               24440000    198901  (52) 
LSST_WFD_MODEL13               10470000     96020  (100) 
LSST_WFD_MODEL14                5967000     46288  (55) 
LSST_WFD_MODEL41                1232000     36418  (63) 
LSST_WFD_MODEL43                8025000     56901  (54) 
LSST_WFD_MODEL45                 104080       210  (0) 
LSST_WFD_MODEL50                   6640        20  (8) 
LSST_WFD_MODEL51                   6640        39  (11) 
LSST_WFD_MODEL60                  84000     32313  (61) 
LSST_WFD_MODEL61                   5240      1044  (0) 
LSST_WFD_MODEL62                4190000      1456  (7) 
LSST_WFD_MODEL63                2626000      8559  (70) 
LSST_WFD_MODEL64                  54240     12656  (6) 
LSST_WFD_MODEL80                 150000     48346  (201) 
LSST_WFD_MODEL81                 100000     14372  (50) 
LSST_WFD_MODEL82                 100000     74205  (115) 
LSST_WFD_MODEL83                  10000      6046  (20) 
LSST_WFD_MODEL90                    280         1  (0) 
LSST_WFD_MODEL91                  30000         0  (0) 
# -------------------------------------------------------------
SUM                           106931120   2591523  (2176) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  41150     13861  (871) 
LSST_DDF_MODEL02                  69760      5073  (258) 
LSST_DDF_MODEL03                  29900      1065  (48) 
LSST_DDF_MODEL12                  69760      5628  (34) 
LSST_DDF_MODEL13                  29900      1208  (73) 
LSST_DDF_MODEL14                  17030       547  (48) 
LSST_DDF_MODEL41                   3510       423  (54) 
LSST_DDF_MODEL43                  22910       871  (65) 
LSST_DDF_MODEL45                    290         3  (0) 
LSST_DDF_MODEL50                     20         0  (0) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    240       137  (54) 
LSST_DDF_MODEL61                     20         9  (0) 
LSST_DDF_MODEL62                  11960        24  (0) 
LSST_DDF_MODEL63                   7490       143  (3) 
LSST_DDF_MODEL64                    150        86  (9) 
LSST_DDF_MODEL80                    150        10  (10) 
LSST_DDF_MODEL81                    100        55  (54) 
LSST_DDF_MODEL82                    150       150  (104) 
LSST_DDF_MODEL83                    150        98  (93) 
LSST_DDF_MODEL90                     20         0  (0) 
LSST_DDF_MODEL91                    100         0  (0) 
# -------------------------------------------------------------
SUM                              304780     29392  (1778) 
 

# ===================================================
        June 25 2018, SNANA v10_60g

   MODEL Updates:
     + AGN : update from Scott. Only 1 galaxy per halo to avoid duplicate
             redshifts. Only 5600 events in library, 1/4 of previous version.
	     Confirmed lack of time lags.
       MODEL84 -> MODEL70 (so that Galactic MODELNUM >=80)

     + RRlyrae updated to remove events with mostly saturations.

     + SNIa: updated t>50 exptrapolation to be based on fitted
         mag/day slopes for mlcs2k2 in the range 45-90 days.
         For next version, may get double-exponential fit from Kaisey.
	 
   SIMULATION UPDATES:
      + for WFD, increase SPEC-TAG by roughly factor of 2 to get closer
        to goal of 5,000 in training set. Classes with very small training
	set get larger pre-scale, and SNIa increase is only x1.5 since
	there are plenty of those already.

      + since previous number of spec-z was > 700,000, here  host-zSpec
        pre-scale is reduced by order of magnitude in WFD.
        N(spec-z) is 11,000 in DDF, 88,000 in WFD.

      + for LCLIB models (Galactic+AGN), each core job starts at random
        position in LCLIB so that the library is uniformly sampled.
        This is particularly helpful for DDF where it's 10 sub-jobs
	had previously sampled the same LCLIB events near the top of
	the library. Bottom line is that AGN redshifts are now randomly
	sampled instead of redshift spikes.

      + updated ZPHOT library from Melissa Graham.

      + Based on discussion with Rafael, implement b-distribution
        for RRLyra using
           http://adsabs.harvard.edu/abs/2017yCat..18380107S
        Apply this distribution to EBE and uLens as well.

        Compute relative WFD/DDF NGEN ratio as follows:
           DDF:  <WGT_SIMLIB> = 0.048610    dOmega = 0.0145
           WFD:  <WGT_SIMLIB> = 0.166368    dOmega = 5.08

        NGENTOT_LC(WFD)/NGENTOT_LC(DDF) = (5.08*0.166368)/(0.0145*0.048610)
	                                = 1200

     + reject events with MWEBV>3; previous cut was MWEBV>1
         from a forgotten default.
     
     + fix subtle sim-bug that could cause negative MWEBV in very-high
       Galactic-extinction regions (MWEBV > 5 ).
    

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  43240     13856  (870) 
LSST_DDF_MODEL02                  69760      4303  (143) 
LSST_DDF_MODEL03                  29900      1793  (98) 
LSST_DDF_MODEL12                  69760      5582  (39) 
LSST_DDF_MODEL13                  29900      1226  (87) 
LSST_DDF_MODEL14                  17030       539  (52) 
LSST_DDF_MODEL41                   3510       413  (58) 
LSST_DDF_MODEL43                  22910       910  (69) 
LSST_DDF_MODEL45                    290         9  (0) 
LSST_DDF_MODEL50                     20         1  (0) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    240       140  (47) 
LSST_DDF_MODEL61                     20         8  (0) 
LSST_DDF_MODEL62                  11960        12  (2) 
LSST_DDF_MODEL63                   7490       138  (6) 
LSST_DDF_MODEL64                    150        83  (7) 
LSST_DDF_MODEL70                    500       484  (108) 
LSST_DDF_MODEL80                    300        82  (80) 
LSST_DDF_MODEL81                    100        44  (40) 
LSST_DDF_MODEL83                    150        80  (74) 
LSST_DDF_MODEL90                     20         0  (0) 
LSST_DDF_MODEL91                     20         0  (0) 
# -------------------------------------------------------------
SUM                              307290     29704  (1780) 


#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               15150000   1481784  (1312) 
LSST_WFD_MODEL02               24440000    299261  (335) 
LSST_WFD_MODEL03               10470000    133961  (182) 
LSST_WFD_MODEL12               24440000    196894  (94) 
LSST_WFD_MODEL13               10470000     95072  (188) 
LSST_WFD_MODEL14                5967000     45861  (96) 
LSST_WFD_MODEL41                1232000     35727  (130) 
LSST_WFD_MODEL43                8025000     56572  (109) 
LSST_WFD_MODEL45                 104080       220  (0) 
LSST_WFD_MODEL50                   6640        30  (11) 
LSST_WFD_MODEL51                   6640        36  (9) 
LSST_WFD_MODEL60                  84000     32414  (95) 
LSST_WFD_MODEL61                   5240      1001  (0) 
LSST_WFD_MODEL62                4190000      1447  (11) 
LSST_WFD_MODEL63                2626000      8346  (53) 
LSST_WFD_MODEL64                  54240     12722  (88) 
LSST_WFD_MODEL70                 175000    123074  (287) 
LSST_WFD_MODEL80                 360000    355834  (267) 
LSST_WFD_MODEL81                 100000     15347  (112) 
LSST_WFD_MODEL83                 180000    115843  (886) 
LSST_WFD_MODEL90                    280       224  (0) 
LSST_WFD_MODEL91                  30000         0  (0) 
# -------------------------------------------------------------
SUM                           108116120   3011670  (4265) 


# ===================================================
        July 15 2018, SNANA v10_60d

           ***** First FINAL Sample for PLASTICC ******
	   
   SIMULATION CHANGES:
      + update observation library (SIMLIB) from Rahul. DDF and WFD
        now have same sky density, where before there was just one
	pointing per DDF field. Rahul also fixed some noise properties.
        SOLID_ANGLE -> 5.47 (was 5.08), or 8% increase.
	
    MODEL UPDATES:
       + new MODEL84, MIRA variables (from Renee), and same b-dependence
         as RRlyrae. Few issues to fix next version:
	  * only 5 library events -> LF is 5 delta functions
	  * periodicity problem at last epoch.
	  * NGEN ?
	  
       + new MODEL91: single-star uLens model (uLens-1STAR)
         from Bachelet, based on GAIA.

   UNRESOLVED ISSUE:
     + For TDE model, the DDF number is 79, which is more than
       order-of-magnitude higher than what we found in DES,
       with similar sensitivity.
       

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  43240     13494  (915) 
LSST_DDF_MODEL02                  69760      4243  (168) 
LSST_DDF_MODEL03                  29900      1774  (97) 
LSST_DDF_MODEL12                  69760      5342  (18) 
LSST_DDF_MODEL13                  29900      1209  (89) 
LSST_DDF_MODEL14                  17030       526  (54) 
LSST_DDF_MODEL41                   3510       380  (71) 
LSST_DDF_MODEL43                  22910       866  (57) 
LSST_DDF_MODEL45                    290         7  (0) 
LSST_DDF_MODEL50                     20         1  (0) 
LSST_DDF_MODEL51                     20         3  (1) 
LSST_DDF_MODEL60                    240       133  (43) 
LSST_DDF_MODEL61                     20         8  (0) 
LSST_DDF_MODEL62                  11960        16  (0) 
LSST_DDF_MODEL63                   7490       142  (0) 
LSST_DDF_MODEL64                    150        79  (14) 
LSST_DDF_MODEL70                    500       478  (105) 
LSST_DDF_MODEL80                    300       234  (75) 
LSST_DDF_MODEL81                    100        51  (48) 
LSST_DDF_MODEL83                    150       101  (90) 
LSST_DDF_MODEL84                     20        20  (0) 
LSST_DDF_MODEL90                     20        19  (0) 
LSST_DDF_MODEL91                     20        16  (11) 
LSST_DDF_MODEL92                     20         0  (0) 
# -------------------------------------------------------------
SUM                              307330     29142  (1856) 


#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               16310000   1446514  (1399) 
LSST_WFD_MODEL02               26320000    305851  (349) 
LSST_WFD_MODEL03               11280000    133406  (202) 
LSST_WFD_MODEL12               26320000    208015  (78) 
LSST_WFD_MODEL13               11280000     90104  (225) 
LSST_WFD_MODEL14                6425000     44902  (90) 
LSST_WFD_MODEL41                1327000     32101  (134) 
LSST_WFD_MODEL43                8641000     56617  (115) 
LSST_WFD_MODEL45                 112080       186  (0) 
LSST_WFD_MODEL50                   7160        22  (9) 
LSST_WFD_MODEL51                   7160        35  (12) 
LSST_WFD_MODEL60                  90440     33121  (114) 
LSST_WFD_MODEL61                   5640      1170  (0) 
LSST_WFD_MODEL62                4511000      1545  (0) 
LSST_WFD_MODEL63                2828000      8342  (0) 
LSST_WFD_MODEL64                  58400     13435  (504) 
LSST_WFD_MODEL70                 175000    118798  (281) 
LSST_WFD_MODEL80                 360000    355811  (281) 
LSST_WFD_MODEL81                 100000     13380  (105) 
LSST_WFD_MODEL83                 180000    117503  (881) 
LSST_WFD_MODEL84                  30000     27218  (33) 
LSST_WFD_MODEL90                    280       236  (0) 
LSST_WFD_MODEL91                   1480       985  (97) 
LSST_WFD_MODEL92                  30000         0  (0) 
# -------------------------------------------------------------
SUM                           116399640   3009297  (4909) 


# ===================================================
        July 27 2018, SNANA v10_60i

       Almost-Final Sample for Kaggle

   CODE UDPATES:
     + Update sim to apply UV-extrapolation to SNIa so that
       that there are no more u or g-band drop outs.
     + fix recent/awful LCLIB bug for Galactic transients
     + correct FLUXCAL for Galactic extinction (OPT_MWEBV: -3)
     + fix code so that SNID(WFD) > 1 million, and thus do not
       overlap with SNID(DDF) < 400000.
     + fix NON-RECUR bug for Galactic models (e.g., uLens)
     + Lots of artifacts found by validation team (Kara,Mia,Gautham...)
       and hopefully fixed. ILOT (MODEL62) truncation not fixed,
       as we are waiting for a response from Ashley.
       
   MODEL UPDATES:
     TDE (MODEL64):
        remove 3 very long-lived SEDs (26,203,316). Asked Ashley
        to investigate.

     MIRA (MODEL84): update from Renee

     uLens_CFA-Binary (MODEL90):
        Update from Rosanne & Arturo with much bigger library.
  
     uLens_CFA-Point (MODEL93)
        New model from Rosanne. Should be analogous to Bachelet's
	MODEL91.
	
    NON1ASED_UV2IR:
        remove AggieNova (SIM_NON1a=270-276) because of very strange
	artifacts in light curves.

    SATURATION:
      increase saturatoin level by 4 mags (100,000 pe -> 3,900,000 pe).
      Motivation is that LSST is attempting to use PSF to recover
      saturated pixels, and we don't want to derail participants
      with saturated epochs. Gautham plans to exclude saturated
      epochs (roughly m<12) when converting data format.	

   uLens Models:
     I spent quite a bit of time checking the CFA models,
     and iterated a few times with them, but please check
     these models. However, beware that some of the events
     have really odd shapes and appear to be artifacts ...
     but are not. So finding genuine artifacts is tougher
     for these. I did not check MODEL91, other than it no
     longer aborts due to having a truncated light curve.


#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  43240     13475  (916) 
LSST_DDF_MODEL02                  69760      4111  (157) 
LSST_DDF_MODEL03                  29900      1027  (62) 
LSST_DDF_MODEL12                  69760      5405  (38) 
LSST_DDF_MODEL13                  29900      1136  (121) 
LSST_DDF_MODEL14                  17030       520  (43) 
LSST_DDF_MODEL41                   3510       380  (71) 
LSST_DDF_MODEL43                  22910       866  (57) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    240       126  (47) 
LSST_DDF_MODEL61                     20        10  (0) 
LSST_DDF_MODEL62                  11960        33  (0) 
LSST_DDF_MODEL63                   7490       142  (0) 
LSST_DDF_MODEL64                    150        65  (3) 
LSST_DDF_MODEL70                    500       481  (101) 
LSST_DDF_MODEL80                    300       300  (94) 
LSST_DDF_MODEL81                    100        42  (38) 
LSST_DDF_MODEL83                    150       133  (126) 
LSST_DDF_MODEL84                     20        20  (7) 
LSST_DDF_MODEL90                     20        10  (0) 
LSST_DDF_MODEL91                     20        14  (6) 
LSST_DDF_MODEL92                      0         0  (0) 
LSST_DDF_MODEL93                     20        13  (5) 
# -------------------------------------------------------------
SUM                              307020     28310  (1892) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               16310000   1447237  (1356) 
LSST_WFD_MODEL02               26320000    319912  (409) 
LSST_WFD_MODEL03               11280000     60561  (138) 
LSST_WFD_MODEL12               26320000    207950  (94) 
LSST_WFD_MODEL13               11280000     89855  (210) 
LSST_WFD_MODEL14                6425000     44602  (78) 
LSST_WFD_MODEL41                1327000     32161  (134) 
LSST_WFD_MODEL43                8641000     56591  (115) 
LSST_WFD_MODEL51                   7160        42  (21) 
LSST_WFD_MODEL60                  90440     33211  (131) 
LSST_WFD_MODEL61                   5640      1178  (0) 
LSST_WFD_MODEL62                4511000      1548  (0) 
LSST_WFD_MODEL63                2828000      8406  (0) 
LSST_WFD_MODEL64                  58400     13358  (456) 
LSST_WFD_MODEL70                 175000    119270  (287) 
LSST_WFD_MODEL80                 360000    359386  (295) 
LSST_WFD_MODEL81                 100000     13256  (94) 
LSST_WFD_MODEL83                 180000    132205  (987) 
LSST_WFD_MODEL84                   1000      1000  (25) 
LSST_WFD_MODEL90                   1000       512  (0) 
LSST_WFD_MODEL91                   1200       694  (80) 
LSST_WFD_MODEL92                      0         0  (0) 
LSST_WFD_MODEL93                   1200       655  (67) 
# -------------------------------------------------------------
SUM                           116223040   2943590  (4977) 


# ===================================================
        Aug 15 2018, SNANA v10_64b

      Cross-our-Fingers Final Sample for Kaggle

   + Reject short seasons (<30 days)

   + Model updates to fix artifacts for
        91(uLens-Binary), 93(uLens-Point): 
	02+03(CC templates)

   + Removed MODEL12(II-PCA) : couldn't remove artifacts in time

+ MODEL02 is now a hybrid from 02+14 (12 removed)   


#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL01                  43240     12848  (860) 
LSST_DDF_MODEL02                 139500      5181  (174) 
LSST_DDF_MODEL03                  29900      1005  (55) 
LSST_DDF_MODEL13                  29900      1131  (122) 
LSST_DDF_MODEL14                  17030       520  (43) 
LSST_DDF_MODEL41                   3510       379  (68) 
LSST_DDF_MODEL43                  22910       854  (55) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    240       126  (46) 
LSST_DDF_MODEL61                     20        10  (0) 
LSST_DDF_MODEL62                  11960        33  (0) 
LSST_DDF_MODEL63                   7490       142  (0) 
LSST_DDF_MODEL64                    150        64  (3) 
LSST_DDF_MODEL70                    500       481  (101) 
LSST_DDF_MODEL80                    200       200  (62) 
LSST_DDF_MODEL81                    200       117  (112) 
LSST_DDF_MODEL83                    150       133  (126) 
LSST_DDF_MODEL84                     20        20  (7) 
LSST_DDF_MODEL90                     20        12  (0) 
LSST_DDF_MODEL91                     20        14  (6) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     20        14  (3) 
# -------------------------------------------------------------
SUM                              307020     23285  (1843) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL01               16310000   1447837  (1284) 
LSST_WFD_MODEL02               52630000    321652  (347) 
LSST_WFD_MODEL03               11280000     58230  (122) 
LSST_WFD_MODEL13               11280000     90520  (220) 
LSST_WFD_MODEL14                6425000     44939  (108) 
LSST_WFD_MODEL41                1327000     32162  (135) 
LSST_WFD_MODEL43                8641000     56591  (114) 
LSST_WFD_MODEL51                   7160        42  (21) 
LSST_WFD_MODEL60                  90440     33210  (130) 
LSST_WFD_MODEL61                   5640      1178  (0) 
LSST_WFD_MODEL62                4511000      1546  (0) 
LSST_WFD_MODEL63                2828000      8402  (0) 
LSST_WFD_MODEL64                  58400     13357  (460) 
LSST_WFD_MODEL70                 175000    119282  (290) 
LSST_WFD_MODEL80                 200000    199636  (160) 
LSST_WFD_MODEL81                 200000     26725  (214) 
LSST_WFD_MODEL83                 180000    132166  (1009) 
LSST_WFD_MODEL84                   1000      1000  (15) 
LSST_WFD_MODEL90                   1000       554  (0) 
LSST_WFD_MODEL91                   1200       669  (74) 
LSST_WFD_MODEL92                  30000         0  (0) 
LSST_WFD_MODEL93                   1200       646  (70) 
# -------------------------------------------------------------
SUM                           116183040   2590344  (4773) 


# ===================================================
        Aug 17 2018, SNANA v10_64b

  Switch cadence from minion to kraken_2026.

  MODEL01 -> MODEL11 (SNIA) so that SNIa model number
  does not match default ITYPE=1 in SNANA manual.

  WFD(Kraken) has 1% fewer events (than minion), but
  10% fewer SPEC events for training.
  

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL02                 156800      4999  (165) 
LSST_DDF_MODEL03                  33610      1003  (60) 
LSST_DDF_MODEL11                  48610     12530  (833) 
LSST_DDF_MODEL13                  33610      1136  (75) 
LSST_DDF_MODEL14                  19140       491  (56) 
LSST_DDF_MODEL41                   3950       367  (51) 
LSST_DDF_MODEL43                  25750       832  (57) 
LSST_DDF_MODEL51                     20         1  (0) 
LSST_DDF_MODEL60                    270       156  (52) 
LSST_DDF_MODEL61                     20        13  (0) 
LSST_DDF_MODEL62                  13440        34  (0) 
LSST_DDF_MODEL63                   8420       158  (0) 
LSST_DDF_MODEL64                    170        79  (11) 
LSST_DDF_MODEL70                    500       464  (99) 
LSST_DDF_MODEL80                    200       200  (61) 
LSST_DDF_MODEL81                    200        78  (64) 
LSST_DDF_MODEL83                    150       124  (120) 
LSST_DDF_MODEL84                     20        20  (9) 
LSST_DDF_MODEL90                     20        13  (0) 
LSST_DDF_MODEL91                     20         8  (4) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     20        15  (9) 
# -------------------------------------------------------------
SUM                              344960     22721  (1726) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL02               52690000    333625  (295) 
LSST_WFD_MODEL03               11290000     61885  (111) 
LSST_WFD_MODEL11               16330000   1400501  (1066) 
LSST_WFD_MODEL13               11290000     91344  (139) 
LSST_WFD_MODEL14                6432000     46024  (67) 
LSST_WFD_MODEL41                1328000     33689  (100) 
LSST_WFD_MODEL43                8650000     57851  (88) 
LSST_WFD_MODEL51                   7160        46  (14) 
LSST_WFD_MODEL60                  90520     29436  (121) 
LSST_WFD_MODEL61                   5640      1134  (0) 
LSST_WFD_MODEL62                4516000      1683  (0) 
LSST_WFD_MODEL63                2831000      8811  (0) 
LSST_WFD_MODEL64                  58480     11660  (373) 
LSST_WFD_MODEL70                 175000    122957  (277) 
LSST_WFD_MODEL80                 200000    199611  (150) 
LSST_WFD_MODEL81                 200000     31530  (235) 
LSST_WFD_MODEL83                 180000    133276  (1035) 
LSST_WFD_MODEL84                   1000      1000  (21) 
LSST_WFD_MODEL90                   1000       519  (0) 
LSST_WFD_MODEL91                   1200       611  (58) 
LSST_WFD_MODEL92                  30000         0  (0) 
LSST_WFD_MODEL93                   1200       600  (68) 
# -------------------------------------------------------------
SUM                           116308200   2567793  (4218) 



# ===================================================
        Aug 25 2018, SNANA v10_64e

  + Cut on 0<HOST_ZPHOT<3 instead of cut on REDSHIFT_FINAL

  + Back to minionv4(recalc), with randomized sky locations

            ***** MODEL updates ******
  + MODEL02 (CC-II): after removing artifact templates, brighten
       by 0.6 mag to match Li 2011 Table 6. Recovers previous rate.

  + MODEL12 (CC-II pca); fix triangle artifact, back in the mix.
     
  + MODEL51 (KN): triple rate to prevent metric-score cheating  

  + MODEL70 (AGN): same photo-z model as other transients
          (i.e., no degradation from AGN activity)
	  
  + MODEL84 (MIRA) more variability
  
  + MODEL11 (SNIa): model number changed from 1 to avoid matching
        SNANA manual for default ITYPE(SNIa)=1
    

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL02                  69810      4807  (195) 
LSST_DDF_MODEL03                  29920      1087  (60) 
LSST_DDF_MODEL11                  43270     13470  (881) 
LSST_DDF_MODEL12                  69810     11089  (154) 
LSST_DDF_MODEL13                  29920      1184  (85) 
LSST_DDF_MODEL14                  17040       522  (49) 
LSST_DDF_MODEL41                   3510       428  (66) 
LSST_DDF_MODEL43                  22920       877  (70) 
LSST_DDF_MODEL51                     50         0  (0) 
LSST_DDF_MODEL60                    240       135  (50) 
LSST_DDF_MODEL61                     10         6  (0) 
LSST_DDF_MODEL62                  11970        28  (0) 
LSST_DDF_MODEL63                   7500       151  (0) 
LSST_DDF_MODEL64                    150        80  (15) 
LSST_DDF_MODEL70                    500       482  (102) 
LSST_DDF_MODEL80                    200       200  (61) 
LSST_DDF_MODEL81                    200        99  (92) 
LSST_DDF_MODEL83                    150       124  (115) 
LSST_DDF_MODEL84                     10        10  (5) 
LSST_DDF_MODEL90                     10         9  (0) 
LSST_DDF_MODEL91                     10         9  (6) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     10         5  (2) 
# -------------------------------------------------------------
SUM                              307230     34802  (2008) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL02               26310000    356551  (420) 
LSST_WFD_MODEL03               11270000     67263  (125) 
LSST_WFD_MODEL11               16310000   1648985  (1463) 
LSST_WFD_MODEL12               26310000    583409  (378) 
LSST_WFD_MODEL13               11270000    106575  (217) 
LSST_WFD_MODEL14                6422000     51808  (94) 
LSST_WFD_MODEL41                1326000     39973  (142) 
LSST_WFD_MODEL43                8638000     62970  (113) 
LSST_WFD_MODEL51                  21520       115  (45) 
LSST_WFD_MODEL60                  90400     35852  (117) 
LSST_WFD_MODEL61                   5640      1168  (0) 
LSST_WFD_MODEL62                4510000      1644  (0) 
LSST_WFD_MODEL63                2827000      9568  (0) 
LSST_WFD_MODEL64                  58400     14043  (495) 
LSST_WFD_MODEL70                 175000    123074  (289) 
LSST_WFD_MODEL80                 200000    198951  (142) 
LSST_WFD_MODEL81                 200000     29920  (217) 
LSST_WFD_MODEL83                 180000    112564  (865) 
LSST_WFD_MODEL84                   1000       998  (17) 
LSST_WFD_MODEL90                   1000       596  (0) 
LSST_WFD_MODEL91                   1200       737  (87) 
LSST_WFD_MODEL92                  30000         1  (0) 
LSST_WFD_MODEL93                   1200       710  (59) 
# -------------------------------------------------------------
SUM                           116158360   3447475  (5285) 


# ===================================================
        Aug 27 2018, SNANA v10_64f

   For KN and CC models, force min mag/day slope for late-time
   extraploation. Avoids a few cases where LC plateaus nearly
   flat and then gets extended forever.
   See new MINSLOPE_EXTRAPMAG_LATE key in SIMGEN_INCLUDE* files.

   MODEL91 uLens_GaiaStar: updated from Gautham with better interpolation.
   
   Code fix for PERIODIC events: apply random phase shift.
   

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL02                  69810      4723  (194) 
LSST_DDF_MODEL03                  29920      1087  (60) 
LSST_DDF_MODEL11                  43270     13470  (881) 
LSST_DDF_MODEL12                  69810     11089  (154) 
LSST_DDF_MODEL13                  29920      1184  (85) 
LSST_DDF_MODEL14                  17040       522  (49) 
LSST_DDF_MODEL41                   3510       428  (66) 
LSST_DDF_MODEL43                  22920       877  (70) 
LSST_DDF_MODEL51                     50         0  (0) 
LSST_DDF_MODEL60                    240       135  (50) 
LSST_DDF_MODEL61                     10         6  (0) 
LSST_DDF_MODEL62                  11970        28  (0) 
LSST_DDF_MODEL63                   7500       151  (0) 
LSST_DDF_MODEL64                    150        80  (15) 
LSST_DDF_MODEL70                    500       482  (102) 
LSST_DDF_MODEL80                    200       200  (49) 
LSST_DDF_MODEL81                    200        99  (92) 
LSST_DDF_MODEL83                    150       124  (117) 
LSST_DDF_MODEL84                     10        10  (4) 
LSST_DDF_MODEL90                     10         9  (0) 
LSST_DDF_MODEL91                     10         9  (6) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     10         5  (2) 
# -------------------------------------------------------------
SUM                              307230     34718  (1996) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL02               26310000    349341  (417) 
LSST_WFD_MODEL03               11270000     67169  (124) 
LSST_WFD_MODEL11               16310000   1648985  (1463) 
LSST_WFD_MODEL12               26310000    583409  (378) 
LSST_WFD_MODEL13               11270000    106575  (217) 
LSST_WFD_MODEL14                6422000     51808  (94) 
LSST_WFD_MODEL41                1326000     39973  (142) 
LSST_WFD_MODEL43                8638000     62970  (113) 
LSST_WFD_MODEL51                  21520       115  (45) 
LSST_WFD_MODEL60                  90400     35852  (117) 
LSST_WFD_MODEL61                   5640      1168  (0) 
LSST_WFD_MODEL62                4510000      1644  (0) 
LSST_WFD_MODEL63                2827000      9568  (0) 
LSST_WFD_MODEL64                  58400     14043  (495) 
LSST_WFD_MODEL70                 175000    123074  (289) 
LSST_WFD_MODEL80                 200000    198954  (154) 
LSST_WFD_MODEL81                 200000     29920  (217) 
LSST_WFD_MODEL83                 180000     97790  (770) 
LSST_WFD_MODEL84                   1000       998  (15) 
LSST_WFD_MODEL90                   1000       596  (0) 
LSST_WFD_MODEL91                   1200       751  (86) 
LSST_WFD_MODEL92                  30000         1  (0) 
LSST_WFD_MODEL93                   1200       710  (59) 
# -------------------------------------------------------------
SUM                           116158360   3425414  (5195) 



# ===================================================
        Aug 30 2018, SNANA v10_64g

   Bug fixes:
     + MWEBV now applied to Galactic transients in simulation
     + MIRA (MODEL84): removed sub-models which had abrupt mag-changes
     + fix SIM_DLMAG for AGN ... has no effect on data, but just
       avoids crazy DLMAG-vs-ZCMB in output.
       
   MODEL70(AGN): use new AGN-specific HOSTLIB to get degraded photo-z.

   Adjust Galactic rates to limit leaderboard cheating.
   (KN rate x2 again, or x4 more than nominal rate estimate)
   

#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL02                  69810      4734  (158) 
LSST_DDF_MODEL03                  29920      1059  (50) 
LSST_DDF_MODEL11                  43270     13477  (837) 
LSST_DDF_MODEL12                  69810     10984  (116) 
LSST_DDF_MODEL13                  29920      1264  (79) 
LSST_DDF_MODEL14                  17040       572  (30) 
LSST_DDF_MODEL41                   3510       428  (66) 
LSST_DDF_MODEL43                  22920       877  (70) 
LSST_DDF_MODEL51                    110         4  (2) 
LSST_DDF_MODEL60                    240       139  (41) 
LSST_DDF_MODEL61                     10         6  (0) 
LSST_DDF_MODEL62                  11970        31  (0) 
LSST_DDF_MODEL63                   7500       142  (0) 
LSST_DDF_MODEL64                    150        76  (8) 
LSST_DDF_MODEL70                    500       485  (117) 
LSST_DDF_MODEL80                    200       200  (58) 
LSST_DDF_MODEL81                    800       370  (309) 
LSST_DDF_MODEL83                    200       165  (162) 
LSST_DDF_MODEL84                     10        10  (4) 
LSST_DDF_MODEL90                     10         9  (0) 
LSST_DDF_MODEL91                     10         8  (4) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     10         5  (3) 
# -------------------------------------------------------------
SUM                              307940     35045  (2114) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL02               26310000    350311  (474) 
LSST_WFD_MODEL03               11270000     66791  (126) 
LSST_WFD_MODEL11               16310000   1648667  (1476) 
LSST_WFD_MODEL12               26310000    583278  (325) 
LSST_WFD_MODEL13               11270000    106464  (229) 
LSST_WFD_MODEL14                6422000     51464  (90) 
LSST_WFD_MODEL41                1326000     39973  (142) 
LSST_WFD_MODEL43                8638000     62970  (113) 
LSST_WFD_MODEL51                  43040       231  (100) 
LSST_WFD_MODEL60                  90400     35819  (134) 
LSST_WFD_MODEL61                   5640      1166  (0) 
LSST_WFD_MODEL62                4510000      1671  (0) 
LSST_WFD_MODEL63                2827000      9538  (0) 
LSST_WFD_MODEL64                  58400     13974  (487) 
LSST_WFD_MODEL70                 175000    101523  (252) 
LSST_WFD_MODEL80                 200000    197194  (181) 
LSST_WFD_MODEL81                 800000     94105  (672) 
LSST_WFD_MODEL83                 220000     99665  (777) 
LSST_WFD_MODEL84                   1480      1475  (26) 
LSST_WFD_MODEL90                   1000       536  (0) 
LSST_WFD_MODEL91                   1400       770  (72) 
LSST_WFD_MODEL92                  30000         0  (0) 
LSST_WFD_MODEL93                   1400       686  (72) 
# -------------------------------------------------------------
SUM                           116820760   3468271  (5748) 


# ===================================================
        Aug 31 2018, SNANA v10_64h
	(2nd serious final sample)

   + use same HOSTLIB for AGN and other extraGalactic
      (no more AGN-specific HOSTLIB)

   + reject events if any mag or template mag < 14 (any band)
     Cut is applied to MWEBV-corrected PEAKMAG and TemplateMag.
     
   + add MWEBV error to FLUXCAL

                               NWRITE         NWRITE
#  GENVERSION          NGEN   (no mag cut)  (all mag>14)  Ncut
# --------------------------------------------------------------
LSST_WFD_MODEL80      200000     197194       197194       0
LSST_WFD_MODEL81      800000      94105        94105       0
LSST_WFD_MODEL83      220000      99665        97331    2334
LSST_WFD_MODEL84        1480       1475         1473       2
LSST_WFD_MODEL90        1000        536          524      12
LSST_WFD_MODEL91        1400        770          766       4
LSST_WFD_MODEL93        1400        686          675      11
# --------------------------------------------------------------

   --> no significant changes with MAG>14 cut.


#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_DDF_MODEL02                  69810      4734  (158) 
LSST_DDF_MODEL03                  29920      1059  (50) 
LSST_DDF_MODEL11                  43270     13477  (837) 
LSST_DDF_MODEL12                  69810     10984  (116) 
LSST_DDF_MODEL13                  29920      1264  (79) 
LSST_DDF_MODEL14                  17040       572  (30) 
LSST_DDF_MODEL41                   3510       428  (66) 
LSST_DDF_MODEL43                  22920       877  (70) 
LSST_DDF_MODEL51                    110         4  (2) 
LSST_DDF_MODEL60                    240       139  (41) 
LSST_DDF_MODEL61                     10         6  (0) 
LSST_DDF_MODEL62                  11970        31  (0) 
LSST_DDF_MODEL63                   7500       142  (0) 
LSST_DDF_MODEL64                    150        76  (8) 
LSST_DDF_MODEL70                    500       482  (119) 
LSST_DDF_MODEL80                    200       200  (58) 
LSST_DDF_MODEL81                    800       370  (309) 
LSST_DDF_MODEL83                    200       165  (162) 
LSST_DDF_MODEL84                     10        10  (4) 
LSST_DDF_MODEL90                     10         9  (0) 
LSST_DDF_MODEL91                     10         8  (4) 
LSST_DDF_MODEL92                     20         0  (0) 
LSST_DDF_MODEL93                     10         5  (3) 
# -------------------------------------------------------------
SUM                              307940     35042  (2116) 
 
#  GENVERSION                      NGEN    NWRITE  (NSPEC) 
# -------------------------------------------------------------
LSST_WFD_MODEL02               26310000    350311  (474) 
LSST_WFD_MODEL03               11270000     66791  (126) 
LSST_WFD_MODEL11               16310000   1648667  (1476) 
LSST_WFD_MODEL12               26310000    583278  (325) 
LSST_WFD_MODEL13               11270000    106464  (229) 
LSST_WFD_MODEL14                6422000     51464  (90) 
LSST_WFD_MODEL41                1326000     39973  (142) 
LSST_WFD_MODEL43                8638000     62970  (113) 
LSST_WFD_MODEL51                  43040       231  (100) 
LSST_WFD_MODEL60                  90400     35818  (134) 
LSST_WFD_MODEL61                   5640      1166  (0) 
LSST_WFD_MODEL62                4510000      1671  (0) 
LSST_WFD_MODEL63                2827000      9538  (0) 
LSST_WFD_MODEL64                  58400     13974  (487) 
LSST_WFD_MODEL70                 175000    101312  (251) 
LSST_WFD_MODEL80                 200000    197194  (181) 
LSST_WFD_MODEL81                 800000     94105  (672) 
LSST_WFD_MODEL83                 220000     97331  (762) 
LSST_WFD_MODEL84                   1480      1473  (26) 
LSST_WFD_MODEL90                   1000       524  (0) 
LSST_WFD_MODEL91                   1400       766  (72) 
LSST_WFD_MODEL92                  30000         0  (0) 
LSST_WFD_MODEL93                   1400       675  (72) 
# -------------------------------------------------------------
SUM                           116820760   3465696  (5732) 

END:

