import System.Environment
import Text.Printf
import qualified Data.Text as T

data Weight = Kg Float | Lb Float | St Float | None

instance Show Weight where
    show (Kg x) = printf "%.2fkg" x
    show (St x) = printf "%.2fst" x
    show (Lb x) = printf "%.2flb" x
    show None = "NO WEIGHT"

to_kg :: Weight -> Weight
to_kg None = None
to_kg (Kg 0) = None
to_kg (Kg x) = Kg x
to_kg (St x) = Kg (x / 2.2 * 14.0)
to_kg (Lb x) = Kg (x / 2.2)

to_lb :: Weight -> Weight
to_lb (Kg x) = Lb( x * 2.2 )
to_lb y = to_lb $ to_kg y

to_st :: Weight -> Weight
to_st (Kg x) = St( x * 2.2 / 14 )
to_st y = to_st $ to_kg y

delta :: Weight -> Weight -> Weight
delta (Kg x) (Kg y) = Kg $ x - y
delta x y = delta (to_kg x) (to_kg y)

weight_from_args :: [String] -> Weight
weight_from_args [] = None
weight_from_args [x] = Kg $ read x
weight_from_args (x:"kg":_) = Kg $ read x
weight_from_args (x:"st":_) = St $ read x
weight_from_args (x:"lb":_) = Lb $ read x

main = do
    args <- getArgs
    let prev = Kg 117
    let now = to_kg . weight_from_args $ args
    let weightstr_diff = show $ delta prev now
    let joined = T.intercalate (T.pack " ") $ map (T.pack . show) [now, to_lb now, to_st now]
    case now of
        None -> putStrLn "Not a valid weight"
        _ -> printf "%s (%s)\n" joined weightstr_diff
