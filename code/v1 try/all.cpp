#include <iostream>
#include <vector>
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <Eigen/SparseLU>
#include <Eigen/SparseQR>
#include <Eigen/IterativeLinearSolvers>
#include <cmath>

// Define base vectors b 
std::vector<double> b_vector_1 = {1.0, 2.0, 3.0};
std::vector<double> b_vector_2 = {1.0, 2.0, 3.0};
std::vector<double> b_vector_3 = {1.0, 2.0, 3.0};
std::vector<double> b_vector_4 = {1.0, 2.0, 3.0};
std::vector<double> b_vector_5 = {1.0, 2.0, 3.0};
std::vector<double> b_vector_6 = {1.0, 2.0, 3.0};

// Define 6 i unit vectors (3D)
std::vector<std::vector<double> i_vectors_1 = {1.0, 0.0, 0.0};
std::vector<std::vector<double> i_vectors_2 = {1.0, 0.0, 0.0};
std::vector<std::vector<double> i_vectors_3 = {1.0, 0.0, 0.0};
std::vector<std::vector<double> i_vectors_4 = {1.0, 0.0, 0.0};
std::vector<std::vector<double> i_vectors_5 = {1.0, 0.0, 0.0};
std::vector<std::vector<double> i_vectors_6 = {1.0, 0.0, 0.0};

// Define force vector
 std::vector<double> force_vector_1 = {1.0};
 std::vector<double> force_vector_2 = {1.0};
 std::vector<double> force_vector_3 = {1.0};
 std::vector<double> force_vector_4 = {1.0};
 std::vector<double> force_vector_5 = {1.0};
 std::vector<double> force_vector_6 = {1.0};


// T transform matrix
 std::vector<std::vector<double> > T_matrix = ;



int main() {
    // Print the 3D vector and the 3D unit vectors
    std::cout << "3D Vector: (" << b_vector[0] << ", " << b_vector[1] << ", " << b_vector[2] << ")" << std::endl;

    // Print the 3D unit vectors
    for (int i = 0; i < 3; i++) {
        std::cout << "3D Unit Vector " << i + 1 << ": (" << i_vectors[i][0] << ", " << i_vectors[i][1] << ", " << i_vectors[i][2] << ")" << std::endl;
    }

    // Print the scalars
    for (int i = 0; i < 6; i++) {
        std::cout << "Scalar " << i + 1 << ": " << scalars[i] << std::endl;
    }

    return 0;
}


// Define transform matrix
Eigen::Matrix3d T_matrix = Eigen::Matrix3d::Identity();

int main() {
    // Print the 3D vector and the 3D unit vectors
    std::cout << "3D Vector: (" << b_vector_1[0] << ", " << b_vector_1[1] << ", " << b_vector_1[2] << ")" << std::endl;

    // Print the 3D unit vectors
    for (int i = 0; i < 3; i++) {
        std::cout << "3D Unit Vector " << i + 1 << ": (" << i_vectors_1[i][0] << ", " << i_vectors_1[i][1] << ", " << i_vectors_1[i][2] << ")" << std::endl;
    }

    // Print the scalars
    for (int i = 0; i < 6; i++) {
        std::cout << "Scalar " << i + 1 << ": " << scalars[i] << std::endl;
    }

    // Define the cross product matrix
    Eigen::Matrix3d cross_product_matrix = Eigen::Matrix3d::Zero();
    cross_product_matrix << 0, -b_vector_1[2], b_vector_1[1],
                                 b_vector_1[2], 0, -b_vector_1[0],
                                 -b_vector_1[1], b_vector_1[0], 0;

    // Calculate the cross product of each base vector with each unit vector
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            Eigen::Vector3d cross_product = cross_product_matrix.col(i) * i_vectors_1[j];
            std::cout << "Cross Product of b_vector_1 and i_vector_" << j + 1 << ": (" << cross_product[0] << ", " << cross_product[1] << ", " << cross_product[2] << ")" << std::endl;
        }
    }

    // Calculate the cross product of each base vector with the negative of each unit vector
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            Eigen::Vector3d cross_product = cross_product_matrix.col(i) * -i_vectors_1[j];
            std::cout << "Cross Product of b_vector_1 and -i_vector_" << j + 1 << ": (" << cross_product[0] << ", " << cross_product[1] << ", " << cross_product[2] << ")" << std::endl;
        }
    }

    // Print the force vector
    for (int i = 0; i < 6; i++) {
        std::cout << "Force Vector " << i + 1 << ": (" << force_vector_1[0] << ", " << force_vector_1[1] << ", " << force_vector_1[2] << ")" << std::endl;
    }

    // Calculate the total force and moment
    Eigen::Vector3d total_force = force_vector_1 + force_vector_2 + force_vector_3 + force_vector_4 + force_vector_5 + force_vector_6;
    double total_moment = 0.0;

    std::cout << "Total Force: (" << total_force[0] << ", " << total_force[1] << ", " << total_force[2] << ")" << std::endl;
    std::cout << "Total Moment: " << total_moment << std::endl;

    return 0;
}