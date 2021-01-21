#import pytaf
#import time





from googletrans import Translator
translator=Translator()
import notam
import parsimonious


s = """(A1912/15 NOTAMN
Q) LOVV/QWPLW/IV/BO/W/000/130/4809N01610E001
A) LOVV B) 1509261100 C) 1509261230
E) PJE WILL TAKE PLACE AT AREA LAAB IN WALDE
PSN:N480930 E0161028 RADIUS - 1NM
F) GND G) FL130)"""


s="""(C1638/20 NOTAMR C1357/20 Q) SLLF/QPDXX/IV/NBO/A/000/999/1658S06508W005  A) SLHI  B) 2008201617  C) 2010202100  E) SUSPENDIDA TEMPO NXT PRFDSGSD GFSDFG FDS)"""


s="""(A3465/19 NOTAMN Q) SPIM/QRALW/IV/NBO/W/000/030/1218S07654W000 A) SPJC  B) 1907251330 C) 1907292000 D) DAYS 25,26,27 AND 29 BTN 1330-2000 E) AIR PARADE DUE TO PERUVIAN INDEPENDENCE DAY. RPAS/DRONES/PARAGLIDERS AND SPORTS ACTIVITIES ARE PROHIBITED. ALL FLT HAVE TO AVOID OVERFLY. PREVIOUS COOR BTN LAS PALMAS TWR AND ACC LIMA IS REQUIRED. COORD: 121806S0765410W 121230S0770340W 120605S077044W 120332S0770238W 120457S0765829W F) GND G) 3000FT)"""

n = notam.Notam.from_str(s)

print("______________________________________", len(s))

print("notam_id")
print(n.notam_id, type(n.notam_id))

print("notam_type")
print(n.notam_type, type(n.notam_type))

print("ref_notam_id")
print(n.ref_notam_id, type(n.ref_notam_id))

print("fir")
print(n.fir, type(n.fir))

print("notam_code")
print(n.notam_code, type(n.notam_code))

print("traffic_type")
print(n.traffic_type, type(n.traffic_type))

print("purpose")
print(n.purpose, type(n.purpose))

print("scope")
print(n.scope, type(n.scope))

print("fl_lower")
print(n.fl_lower, type(n.fl_lower))

print("fl_upper")
print(n.fl_upper, type(n.fl_upper))

print("area")
print(n.area, type(n.area))

print("location")
print(n.location, type(n.location))

print("valid_from")
print(n.valid_from, type(n.valid_from))

print("valid_till")
print(n.valid_till, type(n.valid_till))

print("schedule")
print(n.schedule, type(n.schedule))

print("body")
print(n.body, type(n.body))

print("limit_lower")
print(n.limit_lower, type(n.limit_lower))

print("limit_upper")
print(n.limit_upper, type(n.limit_upper))

print("indices_item_a")
print(n.indices_item_a, type(n.indices_item_a))

print("indices_item_b")
print(n.indices_item_b, type(n.indices_item_b))

print("indices_item_c")
print(n.indices_item_c, type(n.indices_item_c))

print("indices_item_d")
print(n.indices_item_d, type(n.indices_item_d))

print("indices_item_e")
print(n.indices_item_e, type(n.indices_item_e))

print("indices_item_f")
print(n.indices_item_f, type(n.indices_item_f))

print("indices_item_g")
print(n.indices_item_g, type(n.indices_item_g))

'''
print(translator.translate(n.decoded(), dest='es').text)
print(n.decode_abbr(s))
'''

#full_text        # The full text of the NOTAM (for example, when constructed with from_str(s),
#                            #  this will contain s.
#notam_id         # The series and number/year of this NOTAM.
#notam_type       # The NOTAM type: 'NEW', 'REPLACE', or 'CANCEL'.
#ref_notam_id     # If this  NOTAM references a previous NOTAM (notam_type is 'REPLACE' or 'CANCEL'),
#                            #  the series and number/year of the other NOTAM.
#fir              # The FIR within which the subject of the information is located.
#notam_code       # The five-letter NOTAM code, beginning with 'Q'. (Currently a simple str; at some
#                            #  point may be further parsed to specify the code's meaning.)
#traffic_type     # Set of affected traffic. Will contain one or more of:
#                            #  'IFR'/'VFR'/'CHECKLIST'.
#purpose          # Set of NOTAM purposes. Will contain one or more of:
#                            #  'IMMEDIATE ATTENTION'/'OPERATIONAL SIGNIFICANCE'/'FLIGHT OPERATIONS'/
#                            #  'MISC'/'CHECKLIST'.
#scope            # Set of NOTAM scopes. Will contain one or more of:
#                            #  'AERODROME'/'EN-ROUTE'/'NAV WARNING'/'CHECKLIST'.
#fl_lower         # Lower vertical limit of NOTAM area of influence, expressed in flight levels (int).
#fl_upper         # Upper vertical limit of NOTAM area of influence, expressed in flight levels (int).
#area             # Approximate circle whose radius encompasses the NOTAM's whole area of influence.
#                            #   This is a dict with keys: 'lat', 'long', 'radius' (str, str, int respectively).
#location         # List of one or more ICAO location indicators, specifying the aerodrome or FIR
#                            #  in which the facility, airspace, or condition being reported on is located.
#valid_from       # The date and time at which the NOTAM comes into force (datetime.datetime).
#valid_till       # For anything except a 'CANCEL'-type NOTAM, a date and time indicating duration of
#                 #  information (datetime.datetime). If permanent, equal to datetime.datetime.max.
#                 #  If the validity period is estimated, an instance of timeutils.EstimatedDateTime
#                 #  with an attribute 'is_estimated' set to True.
#schedule         # If the condition is active in accordance with a specific time date schedule, an
#                 #  abbreviated textual description of this schedule.
#body             # Text of NOTAM; Plain-language Entry (using ICAO Abbreviations).
#limit_lower      # Textual specification of lower height limit of activities or restrictions.
#limit_upper      # Textual specification of upper height limits of activities or restrictions.
#
## The following contain [start,end) indices for their corresponding NOTAM items (if such exist).
## They can be used to index into Notam.full_text.
#indices_item_a 
#indices_item_b 
#indices_item_c 
#indices_item_d 
#indices_item_e 
#indices_item_f 
#indices_item_g 









'''


taf = pytaf.TAF('SLET 150950Z 1512/1612 18018KT 8000 SCT070 TX33/1519Z TN22/1610Z BECMG 1518/1520 35010KT SCT070 BECMG 1523/1601 NSC')

decoder=pytaf.Decoder(taf)

print(decoder.decode_taf())

print("_______________________________________________________________")

translator=Translator()

print(translator.translate(decoder.decode_taf(), dest='es').text)



print("_______________________________________________________________")

from opensky_api import OpenSkyApi
api = OpenSkyApi()
states=api.get_states()

for i in states.states:
  if i.origin_country in 'Bolivia':
    print(i.latitude, i.longitude)

print(">>>>>>>>" , states.time)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(states.time)))

print("_______________________________________________________________")

import notam

cad="""A0944/20 NOTAMN\nQ) SLLF/QMNXX/IV/NBO/A/000/999/1738S06308W005\nA) SLVR B) 2009161200 C) 2009181800\nD) BTN 1200/1800\nE) CARGO 2 APN MAINT OPS COOR TWR\nCREATED: 11 Sep 2020 20:38:00 \nSOURCE: SLLPYNYX """

n = notam.Notam.from_str(cad)

print(n.valid_from)

print(n.decoded())

'''