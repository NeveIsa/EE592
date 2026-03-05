= EE592 Homework 4

#line(length: 100%)

== Question 4
Prove the uniqueness of the Pseudoinverse lemma

#text(fill: blue)[Let $B_1$ and $B_2$ be two matrices that satisfy the Penrose conditions for $A$. Then $B_1 = B_2$.]


== Solution

=== Penrose conditions:
	1. ABA = A
	2. BAB = B
	3. $(A B)^H = A B$
	4. $(B A)^H = B A$


#underline[Proof of Uniqueness]:

 $ X := A B_1 - A B_2 = A(B_1 - B_2) $

 $ Y := B_1 A - B_2 A = (B_1 - B_2) A $

Note:

$ X^H = (A B_1 - A B_2)^H = (A B_1)^H - (A B_2)^H underbrace(=, "cond. 3") A B_1 - A B_2 = X  \ => X "is hermitian" $

and

$ Y^H = (B_1 A - B_2 A)^H = (B_1 A)^H - (B_2 A)^H underbrace(= , "cond. 4") B_1 A - B_2 A = Y \ => Y "is hermitian" $

Now,

$ X^2 = (A B_1 - A B_2) A (B_1 - B_2) \
    = (A B_1 A - A B_2 A) (B_1 - B_2) \
    = (A - A) (B_1 - B_2) = 0 $

Similarly,

$ Y^2 = (B_1 - B_2) A (B_1 A - B_2 A) \
 = (B_1 - B_2)(A B_1 A -  A B_2 A) \
 = (B_1 - B_2) (A - A) = 0  $


Hence,

$ X^2 = X X = X^H X = 0 \
	=> u^H X^H X u = 0 "  " forall u \
	=> (X u)^H (X u) = 0 \ 
	=> |X u|^2 = 0 \
	=> X u = 0 "  " forall u\
	=> X = 0 \
	=> A B_1 - A B_2 = 0 \
	=> A B_1 = A B_2 "  "#text(fill:red)[      (1)]
$

Similarly, 

$ Y^2 = Y Y = Y^H Y =  0 \
 => u Y^H Y u = 0  "  " forall u \
 => (Y u)^H (Y u) = 0 \
 => |Y u|^2 = 0 \
 => Y u = 0 \
 => Y = 0 \
 => B_1 A - B_2 A = 0 \
 => B_1 A = B_2 A "  "#text(fill:red)[      (2)]
$

Therefore, 

$ B_1 underbrace(=, "cond. 2") B_1 A B_1 underbrace(=, #text(fill: red)[(1)]) B_1 A B_2 underbrace(=, #text(fill: red)[(2)]) B_2 A B_2 underbrace(=, "cond. 2") B_2 \
=> B_1 = B_2 "   " square.filled
$


== Question 5

Prove the following theorem from lecture (DO NOT use the SVD):

#text(fill: blue)[Suppose $B$ is the pseudoinverse of $A$. Then

(a) $A B$ is the projector for  $cal(R)(A)$. \
(b) $B A$ is the projector for $cal(R)(B)$. \
(c) $cal(R)(B) = cal(R)(A^H)$
]

== Solution

An orthogonal projector $P$ on subspace $S$ must satisfy the following conditions - 

1. $cal(R)(P) = S$
2. $P^H = P$
3. $P^2 = P$

(a) We want to show that $P = A B$ is the projector onto $S = cal(R)(A)$.

1. Proof for: $cal(R)( A B) = cal(R)(A)$

$cal(R)(A B) subset cal(R)(A)$ is obvious since $A underbrace(B x, y) = A y in cal(R)(A)$.

For the other direction, assume $y in cal(R)(A)$. Hence $y = A z$ for some $z$.

Now, 

$ #text(fill:green)[$A B y$] = underbrace(A B A, A) z underbrace(=, "cond. 1") A z = y $
$ => y = #text(fill:green)[$A B y$] in cal(R)(A B) $

Hence, $y in cal(R)(A) => y in cal(R)(A B)$ and hence $cal(R)(A) subset cal(R)(A B)$

Since $cal(R)(A B) subset cal(R)(A)$ and $cal(R)(A) subset cal(R)(A B)$, we have $cal(R)(P) = cal(R)(A B) = cal(R)(A)$.

2. $ P^H = (A B)^H underbrace(=, "cond. 3") A B = P $

3. $ P^2 =  ( A B )^2 = underbrace(A B A, A) B underbrace(=, "cond. 1") A B = P $


(b) We want to show $P = B A$ is a projector onto $S = cal(P)(B)$

1. Proof for: $cal(R)(P) = S$

$forall x, "  " P x = B underbrace(A x, y) = B y in cal(R)(B) => cal(R)(P) subset S$ 

For the other direction, assume $y in S = cal(R)(B) => exists z " " s.t " " y = B z$

$B A y = B A B z underbrace(=, "cond. 2") B z = y => y$

Therefore, $ y = B A y in cal(R)(B A) = cal(R)(P) => y in cal(R)(P)$

Hence $y in S => y in cal(R)(P) => S subset cal(R)(P)$

So we have $cal(R)(P) subset S$ and $S subset cal(R)(P)$ which means $cal(R)(P) = S$.

2. $P^H = (B A)^H underbrace(=, "cond. 4") B A = P$

3. $ P^2 = underbrace(B A B, B) A underbrace(=, "cond. 2") =  B A = P$

(c) We want to show $cal(R)(B) = cal(R)(A^H)$

$underline(cal(R)(B) subset.eq cal(R)(A^H))$

Let $z$ be any arbitrary vector in $cal(R)(B)$. Hence there exist $y$ such that $z = B y$.

Now, $z = B y underbrace(=,"cond. 2") B A B y = (B A)^H B y = A^H underbrace(B^H B y,w) = A^H w in cal(R)(A^H)$


$underline(cal(R)(A^H) subset.eq cal(R)(B))$

Let $z$ be any arbitrary vector in $cal(R)(A^H)$. Then $exists y " s.t " z = A^H y$.

Now, $z = A^H y underbrace(=,"cond. 1") (A underline(B A))^H y = (underline(B A))^H A^H y underbrace(=, "cond. 4") B underbrace(A A^H y, w) = B w in cal(R)(B)$
