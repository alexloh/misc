{-
CS386 Programming Languages
Homework 4
Alex Loh
19 Feb 2011
-}

module Lambda where

data Exp = Var String
         | Abs String Exp
         | App Exp Exp
         | Const Int

instance Show Exp where
    show exp = showExp False exp

showExp parens (Var x) = x
showExp parens (Abs x t) = 
   if parens then "(" ++ result ++ ")" else result
      where result = "\\" ++ x ++ "." ++ showExp False t
showExp parens (App (Abs s t) t2) = 
   if parens then "(" ++ result ++ ")" else result
      where result = showExp True (Abs s t) ++ " " ++ showExp True t2
showExp parens (App t1 t2) = 
   if parens then "(" ++ result ++ ")" else result
      where result = showExp False t1 ++ " " ++ showExp True t2



--checks if a term is a value (only used by small-step semantics)
isvalue :: Exp -> Bool
isvalue (Const i)    = True
isvalue (Abs s t) = True
isvalue (Var _) = True
isvalue _            = False

--determines the free variables of term 
freev :: Exp -> [String]
freev (Var s)      = [s]
freev (Const i)    = []
freev (Abs s t) = filter (/= s) (freev t)  --free vars of t except for s (which is bound in the larger term)
freev (App t1 t2)  = freev t1 ++ freev t2

--alpha rename the bound variable of a lambda expression to a name not found in list
--nexts finds the first name s not found in fv by appending increasingly larger integers to s
--note the use of subst within alpha will cascadingly rename BOUND variables within t named news
alpha :: [String] -> Exp -> Exp
alpha fv (Abs s t) = let nexts = \s-> \i-> \fv-> if not (elem (s++show i) fv) 
                                                    then s++show i 
                                                    else nexts s (i+1) fv
                        in let news = nexts s 1 fv
                        in (Abs news (subst s (Var news) t))

--substitutes s for t1 in term, subst s v t2 == [s->v]t2
subst :: String -> Exp -> Exp -> Exp
subst s v (Var x) | x == s    = v
                  | otherwise = (Var x)
subst s v (Const i) = (Const i)
subst s v (Abs y t2) | s == y           = (Abs y t2) --ignore
                     | elem y (freev v) = subst s v (alpha (freev v) (Abs y t2))
                     | otherwise        = (Abs y (subst s v t2))
subst s v (App t2 t3) = (App (subst s v t2) (subst s v t3))



--evals corresponds to the small-step semantics.
{- Calling evals once will only produce one step
Some terms cannot be evaluated according to the small step semantics.
Calling evals on a stuck term will produce an error.-}
{- This implementation is strictly call-by-need,
ie, in (App t1 t2) if t2 is not used in t1, it will never be evaluated.-}
evals :: Exp -> Exp
evals (App t1 t2) | not (isvalue t1) = (App (evals t1) t2)
                  | not (isvalue t2) = (App t1 (evals t2))
evals (App (Abs s t1) t)             = subst s t t1

--evals' corresponds to repeated application of the small-step semantics.
{- If this gets stuck somewhere, the last intermediate term will be returned.-}
evals' :: Exp -> Exp
evals' t | isvalue t    = t     -- value reached, stop
evals' (Var s)          = (Var s)   -- stuck
evals' (App (Var s) t1) = (App (Var s) t1)  -- stuck
evals' t                = evals' (evals t)  -- call evals again



--evalb corresponds to the big-step semantics.
{- Calling evalb on terms that cannot be reduced to a value will result in an error.
Unlike in evals', no 'stuck' intermediate term will ever be produced.-}
{- This implementation is also call-by-need.-}
evalb :: Exp -> Exp
evalb t | isvalue t = t
evalb (App t1 t2)   = v where (Abs s t) = evalb t1
                              v            = evalb (subst s t2 t)


one = Abs "f" (Abs "a" (App (Var "f") (Var "a")))
two = Abs "f" (Abs "a" (App (Var "f") (App (Var "f") (Var "a"))))
plus = Abs "x" (Abs "y" (Abs "f" (Abs "a" (App (App (Var "x") (Var "f")) (App (App (Var "y") (Var "f")) (Var "a"))))))


