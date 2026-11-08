# calculating-volumes-of-regular-polyhedra

Source: https://geometryofthinking.com/2023/10/25/calculating-volumes-of-regular-polyhedra/

When calculating volumes in units of tetrahedra, what would otherwise be perpendicular measurements are instead measured at an angle of atan(√2) from the horizontal. This angle corresponds to the angle the edges of the regular tetrahedron make with their base. Multiplying the perpendicular value, h, by √6/2 gives h’. See Areas and Volumes in Triangles and Tetrahedra.

Polyhedra can be divided up into cones whose bases correspond to the polyhedron’s faces and whose apexes all meet at the polyhedron’s center. This procedure gives the precise volume and, if done correctly, will produce the shorthand formulas that work for all similar polyhedra, as in the following: 

Tetrahedral volume a regular tetrahedron = [edge length]³
Tetrahedral volume a cube = 3×[face diagonal]³
Tetrahedral volume a regular octahedron = 4×[edge length]³
Tetrahedral volume a regular rhombic dodecahedron = 6×[long face diagonal]³
Tetrahedral volume a vector equilibrium (VE) = 20×[edge length]³

The procedures by which the volume formulas are established for these and other polyhedra are demonstrated below. The areas of the faces will mostly be given without showing the work. To learn how each is calculated, see Calculating the Triangular Areas of Regular Polygons.

If the cubic volume of a given polyhedron is known, you can also use a conversion factor to quickly find the equivalent volume in tetrahedra. See General Unit Conversions.

General Volume Formula for all Polyhedra

Given the following parameters:

n = number of faces;
n′ = number of alternate faces (if more than one);
r = in-sphere radius connecting center to its perpendicular with the face;
r′ = in-sphere radius connecting center to alternate faces (if more than one);
a = edge length;
face = area of face (in equilateral triangles);
face′ = area of alternate faces (if more than one),

the general formula for the volume of any polyhedron in cubes is

(n/3)×face (in squares)×r (+ (n’/3)×face′ (in squares)×r′…)

and the general formula for the volume of any polyhedron in regular tetrahedra is 

n×face (in triangles)×r√6/2 (+ n′×face′ (in triangles)×r′√6/2…)

Examples

Volume of Tetrahedron = a³

n = 4
a = edge length
r = a√6/12
face (in squares) = a²√3/4
face (in equilateral triangles) = a²

Volume (in cubes) = n/3×face×r = 4/3×a²√3/4 × a√6/12 = a³/6√2
Volume (in tetrahedra) = n×face×r√6/2 = 4×a²×(a√6/12×√6/2) = a³

Note: The tetrahedron is more sensibly treated as a single cone with a triangular base, in which case the formula becomes:

Volume (in tetrahedra) = base × height × √6/2 = a² × a√6/3 × √6/2 = a³

Volume of Cube (unit diagonal) = 3d³

n = 6
a = edge length
r = a/2
d = diagonal = a√2
a = d√2/2
r = d√2/4
face (in squares) = a² = (d√2/2)² = d²/2
face (in triangles) = 2d²√3/3

Volume (in cubes) = n×face×r = 6×d²/2×d√2/2 = d³√2/4
Volume (in triangles) = n×face×r√6/2 = 6×2d²√3/3×(d√2/4×√6/2) = 3d³

Note: The cube is more sensibly treated as a cylinder with a square base, in which case the formula becomes:

Volume (in tetrahedra) = 3 × base × height × √6/2 = 3 × 2d²√3/3 × d√2/2 × √6/3 = 3d³

For more information on calculating the tetrahedral volumes of cones and cylinders, see Areas and Volumes in Triangles and Tetrahedra.

Volume of Octahedron = 4a³

n = 8
a = edge length
r = a√6/6
face (in squares) = a²√3/4
face (in triangles) = a²

Volume (in cubes) = n/3×face×r = 8/3×a²√3/4×a√6/6 = a³√2/3
Volume (in tetrahedra) = n×face×r√6/2 = 8×a²×a√6/6×√6/2 = 4a³

Volume of Icosahedron = a³φ² × 5√2 -or- d³/φ × 5√2

φ = golden ratio = (1+√5)/2
n = 20
a = edge length
r = a(√3/12)(3+√5) = aφ²√3/6
d = mid-sphere diameter = a × φ
face (in squares) = a²√3/4
face (in triangles) = a²

Volume (in cubes) = n/3×face×r = 20/3×a²√3/4×a(√3/12)(3+√5) = a³×5(3+√5)/12 = a³×5φ²/6
Volume (in tetrahedra) = n×face×r = 20×a²×(a(√3/12)(3+√5)√6/2) = a³×5(3+√5)√2/2 = a³×5φ²√2

Note: Alternately, the tetrahedral volume of the regular icosahedron may be calculated using the edge-to-edge (mid-sphere) diameter, d, or the long edge of golden rectangle used in its construction: d³ × 5√2/φ. When the edge length = 1, d = φ, and the formula becomes 5(φ+1)√2 ≈ 18.51223

Volume of Vector Equilibrium, VE = 20a³

n = 8
n′ = 6
a = edge length

Volume (in cubes) = (n×tetrahedron)+(n′×half octahedron) = (8a³√2/12)+(6a³√2/6) = a³ 5√2/3
Volume (in tetrahedra) = (n×tetrahedron) + (n′×half octahedron) = (8a³)+(6×2a³) = 20a³

Volume of Rhombic Dodecahedron (unit long diagonal) = 6d³

n = 12
d = long diagonal
a = edge length
d = a2√6/3
a = d√6/4
r = a√6/3 = d√6/4×√6/3 = d/2
face (in squares) = 2×a√6/3×a√3/3 = 2×(d√6/4)√6/3 × (d√6/4)√3/3 = d²√2/2
face (in triangles) = 4×a√6/3×a√3/3×2√3/3 = 4×(d√6/4)√6/3×(d√6/4)√3/3×2√3/3 = d²√6/3

Volume (cubes) = n/3×face×r= 12/3 × d²√2/2 × d/2 = d³2√2
Volume (in tetrahedra) = n×face×r√6/2 = 12×d²√6/3×(d/2)√6/2  = 6d³

Volume of Kelvin Truncated Octahedron = 96a³

See also: Kelvin Truncated Octahedron.

n = 6 (square faces)
n’ = 8 (hexagonal faces)
a = edge length
r = a√2 (radius to square face)
r’ = a√6/2 (radius to hexagonal face)
face (square face in squares) = a²
face (square face in equilateral triangles) = a²4√3/3
face’ (hexagonal face in squares) = 6a²√3/4
face’ (hexagonal face in equilateral triangles) = 6a²

Volume (in cubes) = n/3 × face × r = 6/3 × a² × a√2 = 2a³√2
Volume (in tetrahedra) = n × face × r√6/2 = 6 × a²4√3/3 × a√2×√6/2 = 24a³
Volume’ (in cubes) = n’/3 × face’ × r’ = 8/3 × 6a²√3/4 × a√6/2 = 9a³√2
Volume’ (in tetrahedra) = n’ × face’ × r’√6/2 = 8 × 6a² × a√6/2×√6/2 = 72a³
Total Volume (in cubes) = 2a³√2 + 9a³√2 = 11a³√2
Total Volume (in tetrahedra) = 8a³ + 24a³ = 96a³

Volume of Rhombic Triacontahedron = (dφ)³ × 15√2

For a discussion of the 5-tetra-volume rhombic tricontahedron, see T and E Quanta Modules.

n = 30 (rhomboid faces)
d = length of short diagonal
dφ = length of long diagonal
a = edge length = d√(φ+2)/2
d = 2a/√(φ+2)
r = in-sphere radius = dφ²/2
r = in-sphere radius = a√(1+(2/√5))
face (in squares) = d²φ/2
face (in squares) = 2a²√5/5
face (in equilateral triangles) = d²φ × 2√3/3
face (in equilateral triangles) = 8a²√15/15

Volume (in cubes) = 4a³×√(5+2√5)
Volume (in cubes) = n/3 × face × r = 30/3 × d²φ/2 × dφ²/2 = 5(dφ)³/2
Volume (in tetrahedra) = n × face × r√6/2 = [30] × [d²φ × 2√3/3] × [dφ²/2 × √6/2] = 5(dφ)³ × 3√2

Share this:

- 
 Share on X (Opens in new window)
 X
 
- 
 Share on Facebook (Opens in new window)
 Facebook
 
- 

Like Loading...

 Related

 

 
 
 

 
 
 Previous Article Calculating the Triangular Areas of Regular Polygons

 Next Article Areas and Volumes in Triangles and Tetrahedra

 
 
 
 

 
 
 
 Leave a Reply Cancel reply

Comment

Name

Email

Website

 

Turn on JavaScript to leave a comment.

Δ

 

 

 
 
 

 
 Introduction and Index

- About
- Bibliography
- Contact
- Explorations
- Index To Articles
- Model Making
- More Model Making

Articles

- 12-Strut Tensegrity Sphere and its Transformations

- 24-Strut Tensegrity Sphere and its Transformations

- 30-Strut Tensegrity Sphere and its Transformations

- 6-Strut Tensegrity Sphere and its Transformations

- 60-Strut Tensegrity Sphere and its Transformations

- A and B Quanta Modules

- A Curious Helical Structure

- Anatomy of a Sphere

- Areas and Volumes in Triangles and Tetrahedra

- Basic Disequilibrium LCD Triangle

- Basic Equilibrium LCD Triangle

- Blinkers, the Jitterbug, and the “Crystalized” Isotropic Vector Matrix

- Calculating the Tetrahedral Volumes of Regular Polyhedra

- Calculating the Triangular Areas of Regular Polygons

- Categories of Spheres in the Isotropic Vector Matrix: Nuclei, F1 Shells, and “Nuclear Voids”

- Close Packing of Icosahedra

- Close-Packing of Spheres

- Concentric Sphere Shell Growth Rates

- Construction Method for the Pyritohedron and Tetrakaidecahedron of the Weaire-Phelan Structure

- Cube

- Diagonal of the Icosahedron

- Distribution of Radially Close-Packed Spheres on the 25 Axes and Great Circle Planes of the Vector Equilibrium

- Dual Nature of the Tetrahedron

- Equivalence of Tetrahedron Edge Length and Structural Quanta per Volume of its Inscribed Polyhedra

- Formation and Distribution of Nuclei in Radial Close-Packing of Spheres

- General Unit Conversions

- Geodesics

- Golden Ratio

- Great Circle Bow-Ties of the Icosahedron

- Great Circle Bow-Ties of the VE

- Great Circles: Spherical Polyhedra Disclosed by Great Circles of the Icosahedron

- Great Circles: Spherical Polyhedra Disclosed by Great Circles of the VE

- Great Circles: The 25 Great Circles of the Vector Equilibrium (VE)

- Great Circles: The 31 Great Circles of the Icosahedron

- Icosahedron

- Icosahedron Inside Octahedron

- Icosahedron Phases of the Jitterbug

- Inter-Geared Mobilities of the De-Nucleated Vector Equilibrium

- Inter-Sphere Connections via the 25 Great Circles of the VE

- Isotropic Vector Matrix

- Isotropic Vector Matrix as Transverse Waves

- Jessen Orthogonal Icosahedron and Tensor Equilibrium

- Jitterbug

- Jitterbug Animations with Spheres

- Kelvin Truncated Octahedron

- Minimum All-Space-Filling Tetrahedron: “MITE”

- Multiplication and Merger of Spheres in the Jitterbug

- Octahedron

- Operational Geometry

- Pentagonal Dodecahedron

- Pi and the Synergetics Constants

- Polyhedra From Polygonal Strips

- Polyhedra With Whole Number Volumes

- Pyritohedron Dimensions and Whole-Number Volume

- Quanta Module Constructions of the Rhombic Dodecahedron

- Rhombic Dodecahedron

- Rhombic Triacontahedron

- S Quanta Module*

- Seven Axes of Symmetry

- Space-Filling Polyhedra as Close-Packed Spheres

- Spaces and Spheres (Redux)

- Spheres and Spaces

- T and E Quanta Modules

- Tensegrity

- Tensegrity Equilibrium and Vector Equilibrium

- Tensegrity Sphere Equations

- Tetrahedron

- Tetrahelix

- Tetrakaidecahedron and Pyritohedron

- Tetrakaidecahedron Dimensions and Whole Number Volume

- The 25 Great Circles of the VE (new illustrations)

- The 31 Great Circles of the Icosahedron (new illustrations)

- The Jessen Orthogonal Icosahedron in the Isotropic Vector Matrix

- The Polar Pump Model of the Jitterbug

- There’s Just One Way to Stack Cannonballs

- Topological Abundance Formulas

- Twoness: The Multiplicative and Additive Two

- Unique Properties of the Tetrahedron

- Vector Equilibrium and the “VE”

Articles by Date

 
- April 2026
 
- November 2025
 
- September 2025
 
- July 2025
 
- May 2025
 
- April 2025
 
- March 2025
 
- February 2025
 
- January 2025
 
- March 2024
 
- February 2024
 
- December 2023
 
- November 2023
 
- October 2023
 
- September 2023
 
- August 2023
 
- March 2023
 
- January 2023
 
- April 2022
 
- March 2022
 
- February 2022
