import List hiding (union)

instance Eq a => Eq (Set a) where
	(==) = eqSet


instance Ord a => Ord (Set a) where
	(<=) = leqSet

newtype Set a = SetI [a]


