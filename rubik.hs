{-# LANGUAGE GeneralizedNewtypeDeriving #-}
import Data.Semigroup

data Color = Color Int Int Int deriving (Show)

b = Color 1 0 0
y = Color 0 1 0
o = Color 0 0 1
g = Color (-1) 0 0
w = Color 0 (-1) 0
r = Color 0 0 (-1)


-- instance Num Color where
    -- (+) a b = b
    -- (+) (Color a b c) (Color x y z) = Color (a + x) (b + y) (c + z)

-- f :: Color a => a -> a -> a
f :: Color -> Color -> Color
f (Color a b c) (Color x y z) = Color (a + x) (b + y) (c + z)


apply_ _ [] i = i
apply_ start [x] i
    | x == i = start
    | otherwise = i
apply_ start (x:y:xs) i
    | x == i = y
    | otherwise = apply_ start (y:xs) i

apply [] i = i
apply (x:xs) i = apply_ x (x:xs) i
