data Side = F | B deriving (Show)-- front | back

data Axis = X | Y | Z deriving (Show)

-- data Point = Point Int Int Int 
-- 
-- rotation_x :: Point -> Point
-- rotation_x (Point x y z) = Point x z (-y)
-- 
-- rotation_y :: Point -> Point
-- rotation_y (Point x y z) = Point z y (-x)
-- 
-- rotation_z :: Point -> Point
-- rotation_z (Point x y z) = Point y (-x) z

type Point = (Int, Int, Int)


data Color = Color (Int, Int, Int) (Int, Int, Int)
    deriving (Show)


take_coord :: Axis -> Point -> Int
take_coord X (x, _, _) = x
take_coord Y (_, y, _) = y
take_coord Z (_, _, z) = z

under_rotation :: Axis -> Side -> Point -> Bool
under_rotation axis F triplet = (<) 0 $ take_coord axis triplet
under_rotation axis B triplet = (>) 0 $ take_coord axis triplet


apply_to_axis :: Axis -> (Point -> Point) -> Point -> Point
apply_to_axis X f triplet = f triplet
apply_to_axis Y f (x, y, z) = (xa, ya, za)
    where
        (ya, xa, za) = f (y, x, z)
apply_to_axis Z f (x, y, z) = (xa, ya, za)
    where
        (za, xa, ya) = f (z, x, y)


base_rotate :: Side -> Point -> Point
base_rotate F (x, y, z) = (x, z, -y)
base_rotate B (x, y, z) = (x, -z, y)

point_action :: Axis -> Side -> Point -> Point
point_action axis side triplet
    | under_rotation axis side triplet = apply_to_axis axis (base_rotate side) triplet
    | otherwise = triplet


is_identical :: Color -> Bool
is_identical (Color (xl, yl, zl) (xr, yr, zr))
    | xl /= xr = False
    | yl /= yr = False
    | zl /= zr = False
    | otherwise = True


type Colored = [Color]
type Move = Point -> Point

apply_to_color :: Move -> Color -> Color
apply_to_color f (Color point_l point_r) = Color (f point_l) point_r

apply :: Move -> Colored -> Colored
apply f [] = []
apply f (x:xs) = (apply_to_color f x):(apply f xs)


type Letter = (Axis, Side)
type GWord = [Letter]

points_list = [(x, y, z) | x <- [-1, 0, 1], y <- [-1, 0, 1], z <- [-1, 0, 1]]
cube = [Color p p | p <- points_list]

apply_word :: GWord -> Colored -> Colored
apply_word [] !xs = xs
apply_word ((axis, side):moves) !xs = apply_word moves $ apply (point_action axis side) xs

make_index :: Point -> Int
make_index (x, y, z) = (mod x 3) + (mod y 3) * 3 + (mod z 3) * 9

pairs :: Colored -> [(Int, Int)]
pairs [] = []
pairs ((Color p q):xs)
    | p == q = pairs xs
pairs ((Color p q):xs) = (p', q') : pairs xs--  (make_index p, make_index q) : pairs xs
    where
        p' = make_index p
        q' = make_index q


type Transaction = (Int, Int)


search_circle :: [Int] -> [Transaction] -> [Transaction] -> ([Int], [Transaction])
search_circle xs trans [] = (reverse xs, trans)
search_circle [] trans ((e,s):pairs) = search_circle [e, s] trans pairs
search_circle (x:xs) trans ((e,s):pairs)
    | s == x = search_circle (e:x:xs) trans pairs
    | otherwise = search_circle (x:xs) ((e,s):trans) pairs


cicles :: [Transaction] -> [[Int]]
cicles [] = []
cicles xs = c:cicles xs'
    where
        (c, xs') = search_circle [] [] xs

some_word = [(X, F), (X, B), (Y, F), (Y, B), (Z, B), (Z, B)]
-- some_word = [(X, F), (Y, F), (X, F), (X, F), (X, F)]
arr = apply_word some_word cube

trivial_coloring :: Colored -> Bool
trivial_coloring [] = True
trivial_coloring ((Color p q):xs)
    | p == q = trivial_coloring xs
    | otherwise = False

degree_ :: GWord -> Int -> Colored -> Int
degree_ word k manifold
    | trivial_coloring manifold = k
    | otherwise = degree_ word (k+1) $ apply_word word manifold

degree :: GWord -> Int
degree word = degree_ word 1 $ apply_word word cube


r_group = [(X, F), (X, B), (Y, F), (Y, B), (Z, F), (Z, B)]



type Condition = (Colored, GWord)

is_trivial :: Condition -> Bool
is_trivial (manifold, _) = trivial_coloring manifold

separate :: [Condition] -> [Condition] -> [Condition] -> ([Condition], [Condition])
separate xs ys [] = (xs, ys)
separate xs ys (z:zs)
    | is_trivial z = separate (z:xs) ys zs
    | otherwise = separate xs (z:ys) zs

apply_letter_ :: Letter -> Colored -> Colored
apply_letter_ (axis, side) manifold = apply (point_action axis side) manifold


apply_letter :: Condition -> Letter -> Condition
apply_letter (manifold, word) letter = (apply_letter_ letter manifold, letter:word)

condition_word :: Condition -> GWord
condition_word (_, word) = reverse word


splitter :: Int -> ([Condition], [Condition]) -> ([Condition], [Condition])
splitter 0 pair = pair
splitter k (xs, []) = (xs, [])
splitter k (xs, ys) = splitter (k-1) (xs', ys')
    where
        (xs', ys') = separate xs [] $ [apply_letter y l | y <- ys, l <- r_group]
