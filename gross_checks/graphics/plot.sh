for f in dvidtt_h.s frzmlt_h.s daidtd_h.s daidtt_h.s fresh_h.s sice_h.s uatm_h.s congel_h.s snoice_h.s dvidtd_h.s scale_factor_h.s fswdn_h.s hi_h.s vocn_h.s strairx_h.s meltb_h.s fsens_h.s vatm_h.s sst_h.s dsnow_h.s strocnx_h.s strairy_h.s uvel_h.s Qref_h.s fsalt_h.s meltl_h.s meltt_h.s strocny_h.s uocn_h.s fbot_h.s fswabs_h.s vvel_h.s flat_h.s fhocn_h.s shear_h.s melts_h.s evap_h.s hpond_h.s hs_h.s divu_h.s Tair_h.s ipond_h.s Tref_h.s flwup_h.s flwdn_h.s
do
  t=`echo $f | cut -f1`
  python3 plot_errs.py $f $t 12
done
