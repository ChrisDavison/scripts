import System.Environment
import Text.Printf

data Weight = Kg Float | Lb Float | St Float | None

instance Show Weight where
    show (Kg x) = (printf "%.1fkg" x)
    show (St x) = (printf "%.1fst" x)
    show (Lb x) = (printf "%.1flb" x)
    show None = "NO WEIGHT"

to_kg :: Weight -> Weight
to_kg (Kg x) = Kg x
to_kg (St x) = Kg (x / 2.2 * 14.0)
to_kg (Lb x) = Kg (x / 2.2)
to_kg None = Kg 0

delta :: Weight -> Weight -> Weight
delta (Kg x) (Kg y) = Kg $ x - y
delta (St x) (St y) = Kg $ x - y
delta (Lb x) (Lb y) = Kg $ x - y
delta x y = delta (to_kg x) (to_kg y)

weight_from_args :: [String] -> Weight
weight_from_args [] = None
weight_from_args [x] = Kg $ read x
weight_from_args (x:"kg":xs) = Kg $ read x
weight_from_args (x:"st":xs) = St $ read x
weight_from_args (x:"lb":xs) = Lb $ read x

main = do
    args <- getArgs
    let prev = Kg 117
    let now = to_kg $ weight_from_args args
        weightstr now = show prev ++ " -> " ++ show now ++ " (" ++ (show $ delta prev now )++ ")"
    putStrLn $ weightstr now
