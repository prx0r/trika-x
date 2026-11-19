/- Mutation: the inner instruments are listed with only manas and ahaṃkāra
   (buddhi dropped), so the city has seven constituents. The same by-decide
   theorem as in Puryastaka.lean must fail for exactly this reason. -/
namespace FormalTrika

inductive Constituent where
  | sound | touch | form | taste | smell
  | manas | ahankara | buddhi
  deriving DecidableEq, Repr

open Constituent

def tanmatras : List Constituent := [.sound, .touch, .form, .taste, .smell]

def antahkarana : List Constituent := [.manas, .ahankara]  -- deliberate omission

def constituents : List Constituent := tanmatras ++ antahkarana

theorem constituents_eight : constituents.length = 8 := by decide

end FormalTrika
