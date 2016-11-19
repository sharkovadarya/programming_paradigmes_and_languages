-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' (x:_) = x

-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]
tail' [] = []
tail' (x:xs) = xs

-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' n _
    | n <= 0   = []
take' n []     = []
take' n (x:xs) = x : take' (n - 1) xs

-- length' возвращает длину списка
length' :: [a] -> Int
length' [] = 0
length' (x:xs) = 1 + length xs

-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины -- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' _ [] = []
drop' n xs | n <= 0 = xs
drop' n (_:xs) = drop' (n - 1) xs

-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' f xs = [ x | x <- xs, f x]

-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению, полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)   
-- foldl' (*) 4 [] == 4
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

-- flip' возвращает функцию, поменяв местами аргументы
flip' :: (a -> b -> c) -> b -> a -> c
flip' f x y = f y x

-- reverse' возвращает список в обратном порядке
reverse' :: [a] -> [a]
reverse' = foldl' (flip' (:)) []

-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' xs ys = foldl' (flip' (:)) ys (reverse' xs)

-- 8. quickSort' возвращает его отсортированный список (0,5)
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = concat' (quickSort' a) [x] (quickSort' b)
    where a = filter' (<= x) xs
          b = filter' (> x) xs


