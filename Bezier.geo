//                                                           ---------
// ------------------------------------------------------- // OPTIONS //
//                                                           ---------

//                                                        ------------
// ---------------------------------------------------- // PARAMETERS //
//                                                        ------------
xcenter = 25. ; 
ycenter = 25. ;
r = 10.5 ;
edgesize = 1. ;

//                                                              ------
// ---------------------------------------------------------- // MESH //
//                                                              ------

Point(1) = {xcenter     , ycenter    , 0, edgesize};
Point(2) = {xcenter + r + 5 , ycenter    , 0, edgesize};
Point(3) = {xcenter     , ycenter + r, 0, edgesize};
Point(4) = {xcenter - r , ycenter    , 0, edgesize};
Point(5) = {xcenter     , ycenter - r, 0, edgesize};

BSpline(10) = {2,3,4,5, 2};
Line Loop(100) = {10};
Plane Surface(11) = {100};