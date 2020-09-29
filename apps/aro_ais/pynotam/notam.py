from apps.aro_ais.pynotam import timeutils
from apps.aro_ais.pynotam import _abbr
import re as _re
from apps.aro_ais.pynotam import _parser
from io import StringIO as _StringIO


def run():
    print("Test")

class Notam(object):
    def __init__(self):
        self.full_text = None       # The full text of the NOTAM (for example, when constructed with from_str(s),
                                    #  this will contain s.
        self.notam_id = None        # The series and number/year of this NOTAM.
        self.notam_type = None      # The NOTAM type: 'NEW', 'REPLACE', or 'CANCEL'.
        self.ref_notam_id = None    # If this  NOTAM references a previous NOTAM (notam_type is 'REPLACE' or 'CANCEL'),
                                    #  the series and number/year of the other NOTAM.
        self.fir = None             # The FIR within which the subject of the information is located.
        self.notam_code = None      # The five-letter NOTAM code, beginning with 'Q'. (Currently a simple str; at some
                                    #  point may be further parsed to specify the code's meaning.)
        self.traffic_type = None    # Set of affected traffic. Will contain one or more of:
                                    #  'IFR'/'VFR'/'CHECKLIST'.
        self.purpose = None         # Set of NOTAM purposes. Will contain one or more of:
                                    #  'IMMEDIATE ATTENTION'/'OPERATIONAL SIGNIFICANCE'/'FLIGHT OPERATIONS'/
                                    #  'MISC'/'CHECKLIST'.
        self.scope = None           # Set of NOTAM scopes. Will contain one or more of:
                                    #  'AERODROME'/'EN-ROUTE'/'NAV WARNING'/'CHECKLIST'.
        self.fl_lower = None        # Lower vertical limit of NOTAM area of influence, expressed in flight levels (int).
        self.fl_upper = None        # Upper vertical limit of NOTAM area of influence, expressed in flight levels (int).
        self.area = None            # Approximate circle whose radius encompasses the NOTAM's whole area of influence.
                                    #   This is a dict with keys: 'lat', 'long', 'radius' (str, str, int respectively).
        self.location = None        # List of one or more ICAO location indicators, specifying the aerodrome or FIR
                                    #  in which the facility, airspace, or condition being reported on is located.
        self.valid_from = None      # The date and time at which the NOTAM comes into force (datetime.datetime).
        self.valid_till = None      # For anything except a 'CANCEL'-type NOTAM, a date and time indicating duration of
                                    #  information (datetime.datetime). If permanent, equal to datetime.datetime.max.
                                    #  If the validity period is estimated, an instance of timeutils.EstimatedDateTime
                                    #  with an attribute 'is_estimated' set to True.
        self.schedule = None        # If the condition is active in accordance with a specific time date schedule, an
                                    #  abbreviated textual description of this schedule.
        self.body = None            # Text of NOTAM; Plain-language Entry (using ICAO Abbreviations).
        self.limit_lower = None     # Textual specification of lower height limit of activities or restrictions.
        self.limit_upper = None     # Textual specification of upper height limits of activities or restrictions.

        # The following contain [start,end) indices for their corresponding NOTAM items (if such exist).
        # They can be used to index into Notam.full_text.
        self.indices_item_a = None
        self.indices_item_b = None
        self.indices_item_c = None
        self.indices_item_d = None
        self.indices_item_e = None
        self.indices_item_f = None
        self.indices_item_g = None


    def decoded(self):
        """Returns the full text of the NOTAM, with ICAO abbreviations decoded into their un-abbreviated
        form where appropriate."""

        with _StringIO() as sb:
            indices = [getattr(self, 'indices_item_{}'.format(i)) for i in ('d', 'e', 'f', 'g')]
            indices = [i for i in indices if i is not None]
            indices.sort() # The items should already be listed in the order of their apperance in the text, but
                           # we sort them here just in case
            indices = [(0, 0)] + indices + [(-1, -1)]

            for (cur, nxt) in zip(indices, indices[1:]):
                (cs, ce) = cur
                (ns, ne) = nxt
                sb.write(self.decode_abbr(self.full_text[cs:ce]))   # decode the text of this range
                sb.write(self.full_text[ce:ns])                     # copy the text from end of current range to start
                                                                    # of next verbatim
            return sb.getvalue()


    @staticmethod
    def from_str(s):
        """Returns a Notam containing information parsed from within the provided string."""
        n = Notam()
        visitor = _parser.NotamParseVisitor(n)
        visitor.parse(s)
        return n

    @staticmethod
    def decode_abbr(txt):
        """Decodes ICAO abbreviations in 'txt' to their un-abbreviated form."""
        if not getattr(Notam.decode_abbr, 'regex', False):
            Notam.decode_abbr.regex = _re.compile(r'\b(' +
                                                  '|'.join([_re.escape(key) for key in _abbr.ICAO_abbr.keys()]) +
                                                  r')\b')
        return Notam.decode_abbr.regex.sub(lambda m: _abbr.ICAO_abbr[m.group()], txt)