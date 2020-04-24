namespace Quantum.Hydrogen {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Measurement;

    operation QuantumMain() : Unit {
   //-----HydrogenEntanglement() operation, providing an angle and number of iterations-----//
 //-----Defining the state of this wavefunction requires only a single angle parameter,----//
//-----thanks to the well-prepared entangling block in the Parameterize() operation.------//


//---These are the coefficients A, H0, H1, Jx, Jy, Jz from the molecular energy expression.---//
        let parameter = 0.0;
        let coeff = [0.2252, 0.3435, -0.4347, 0.5716, 0.0910, 0.0910];

//---The main operation runs the HydrogenEnergy() operation, provided a parameter, a number of iterations, and the energy coefficients.---//
        let energy = HydrogenEntanglement(parameter, 50, coeff);
        Message($"Energy: {energy}");
    }
    
//-----The Parameterize() function is a series of operations that prepares the highly entangled electronic states of a molecule.----//
    operation Parameterize(q : Qubit[], parameter : Double) : Unit {
        X(q[0]);
        Rx(-PI()/2.0, q[0]);
        Ry(PI()/2.0, q[1]);
        CNOT(q[1], q[0]);
        Rz(parameter, q[0]); //-----The Rz() operation rotates the state to explore this space of quantum states to find the minimum.------//
        CNOT(q[1], q[0]);
        Rx(PI()/2.0, q[0]);
        Ry(-PI()/2.0, q[1]);    
    }
    
    operation HydrogenEntanglement(parameter : Double, iterations : Int, coeff : Double[]) : Double {
        // Define a mutable variable to keep a running total for averaging
        mutable sum = 0.0;

        // Define three mutable arrays for calculating spins along different directions
        //--Mutable arrays are needed to keep track of the x-, y-, and z-aligned spin values for each iteration--//
        mutable z = new Double[2];
        mutable x = new Double[2];
        mutable y = new Double[2];

        using ( q = Qubit[2] ) {
            // Allocate an array of qubits that begin in the |000> state
            for (iter in 1..iterations) { //The operation allocates two qubits to be used throughout each iteration.
                // Rotate the state of each qubit
                Parameterize(q, parameter); //The qubits are prepared into the entangled state parameterized by the rotation parameter.

                // For each qubit, measure the state along the x axis and convert it to a spin value x[i]
                for (i in 0..1) {
                    let result = MResetX(q[i]); //Each qubit is measured along the xx-axis, and then reset and parameterized again.
                    set x w/= i <- IntAsDouble(2 * ResultArrayAsInt([result]) - 1);
                }

                Parameterize(q, parameter);

                // For each qubit, measure the state along the y axis and convert it to a spin value y[i]
                for (i in 0..1) {
                    let result = MResetY(q[i]); //Each qubit is measured along the yy-axis, and then reset and parameterized again.
                    set y w/= i <- IntAsDouble(2 * ResultArrayAsInt([result]) - 1);
                }

                Parameterize(q, parameter);

                // For each qubit, measure the state along the z axis and convert it to a spin value z[i]
                for (i in 0..1) {
                    let result = MResetZ(q[i]); //Each qubit is measured along the zz-axis, and then reset.
                    set z w/= i <- IntAsDouble(2 * ResultArrayAsInt([result]) - 1);
                }

                // Calculate the total energy from the spin values
                let energy = coeff[0] + coeff[1] * z[0] + coeff[2] * z[1] + coeff[3] * z[0] * z[1] + coeff[4] * x[0] * x[1] + coeff[5] * y[0] * y[1];
                set sum = sum + energy; //The energy is calculated according to the molecular energy expression.
            }
        }
        let average = sum/IntAsDouble(iterations);
        return average;
    }
}