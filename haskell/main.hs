binary :: (Ord a ) => a->[a] ->Maybe a 
binary _ [] = Nothing
binary x xs = binary x xs 0 (length xs -  1 )
    where 
        binary x xs low high
            |low > high = Nothing
            |midValue == x = Just midValue
            |midValue < x = binary x xs (mid + 1 ) high
            |otherwise = binary x xs low (mid - 1 )
            where
                    mid = (low + high) `div` 2
                    midValue = xs !! mid 
                    
factorial :: Integer -> Integer 
factorial 0 = 1 
factorial n = n* factorial (n - 1)
 
fibbor :: Integer -> Integer
fibbor 0 = 0 
fibbor 1 = 1 
fibbor n = fibbor (n - 1) + fibbor (n - 2) 

gcds :: Integer -> Integer -> Integer
gcds a 0 = a 
gcds a b = gcds b (a `mod` b) 

bubblesort :: (Ord a ) => [a] -> [a]
bubblesort [] = [] 
bubblesort [x] = [x]
bubblesort (x:y:xs)
    | x > y = y : bubblesort (x : xs)
    | otherwise = x : bubblesort (y : xs)

mergesort :: (Ord a ) => [a] -> [a]
mergesort [] = [] 
mergesort [x] = [x]
mergesort xs = merge (mergesort left) (mergesort right)
    where 
        (left , right) = splitAt (length xs `div` 2 ) xs 
        merge [] ys = ys 
        merge xs [] = xs
        merge (x:xs) (y:ys)
            | x<=y = x : merge xs (y:ys)
            | otherwise = y : merge (x:xs) ys 
binarySearch :: (Ord a) => [a] -> a -> Maybe Int 
binarySearch xs x = binarySearches 0 (length xs - 1 )
    where
        binarySearches low high 
            | low > high = Nothing
            | midElem == x = Just mid 
            | midElem < x = binarySearches (mid + 1 ) high
            | otherwise = binarySearches low (mid -1)
            where 
                    mid = (low+high) `div` 2 
                    midElem = xs !! mid 
prodlist :: Num a => [a] -> a 
prodlist = product
sumlist::Num a =>[a]->a 
sumlist = foldl (+) 0 

data Person = Person   {
   name :: String
   ,age :: Int
} deriving Show
euclid :: Int ->Int ->Int
euclid a 0 = a 
euclid a b = euclid b (a `mod` b)
main :: IO ()
main= do
    print(length [1,2,3])
