# lateral-pile-response-Np-z
Python Code used in master thesis to calculate the lateral response of monopile under combined lateral and torsional force

- The master thesis consisted of a 3d model created in Plaxis 3D, a finite element software used in geotechnical projects im the domain of the civil engineer.
- This 3d model cosisted of a monopile in undrained soil and it is brought to failure with a lateral force while also being influenced by a simultaneous torsional force.
- The mesh of the monopile was constructed so that the pile is divided into layers pf specific depth, that consist of a predetermined amount of triangular element with 6 nodes.
- After the 3d mesh was calculated, this **Python** script was used through the plaxis 3D API to create graphs that show the lateral response coefficient Np in relation to the depth of the monopile.
- The script extracts the normal and shear stresses of each triangular element from Gauss points and extrapolates them to the nodes of said element.
- After that it integrates them to the area of said element and creates the force applied to the specific node.
- After calculating all the forces, they were distributed along the axis of the monopile in order to find the deistributed responde of the monopile and from there the lateral response coefficient.
- In the end the results were saved in an csv file.
