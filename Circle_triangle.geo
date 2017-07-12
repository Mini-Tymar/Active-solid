//                                                           ---------
// ------------------------------------------------------- // OPTIONS //
//                                                           ---------

//                                                        ------------
// ---------------------------------------------------- // PARAMETERS //
//                                                        ------------
xcenter = 50. ; 
ycenter = 50. ;
r = 21. ;
edgesize = 1. ;

//                                                              ------
// ---------------------------------------------------------- // MESH //
//                                                              ------

Point(1) = {xcenter     , ycenter    , 0, edgesize};
Point(2) = {xcenter + r , ycenter    , 0, edgesize};
Point(3) = {xcenter     , ycenter + r, 0, edgesize};
Point(4) = {xcenter - r , ycenter    , 0, edgesize};
Point(5) = {xcenter     , ycenter - r, 0, edgesize};

//           First, Center, Last
Circle(1) = {2    , 1     , 3};
Circle(2) = {3    , 1     , 4};
Circle(3) = {4    , 1     , 5};
Circle(4) = {5    , 1     , 2};

Line Loop(1) = {2,3,4,1};
Plane Surface(1) = {1};