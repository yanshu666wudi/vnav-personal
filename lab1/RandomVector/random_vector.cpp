#include "random_vector.h"
#include <cstdlib>

using namespace std;
RandomVector::RandomVector(int size, double max_val) { 
   for (int i = 0; i < size; i++) {
    double random_value;

    random_value = (double)rand() / RAND_MAX;
    random_value = random_value * max_val;

    vect.push_back(random_value);
  }
}

void RandomVector::print(){
  int number_count = (int)vect.size();

  for (int i = 0; i < number_count; i++) {
    cout << vect[i] << " ";
  }

  cout << endl;
}

double RandomVector::mean(){
  double total_value = 0.0;
  int number_count = (int)vect.size();

  for (int i = 0; i < number_count; i++) {
    total_value = total_value + vect[i];
  }

  return total_value / number_count;
}

double RandomVector::max(){
  int number_count = (int)vect.size();
  double maximum_value = vect[0];

  for (int i = 1; i < number_count; i++) {
    if (vect[i] > maximum_value) {
      maximum_value = vect[i];
    }
  }

  return maximum_value;
}

double RandomVector::min(){
  int number_count = (int)vect.size();
  double minimum_value = vect[0];

  for (int i = 1; i < number_count; i++) {
    if (vect[i] < minimum_value) {
      minimum_value = vect[i];
    }
  }

  return minimum_value;
}

void RandomVector::printHistogram(int bins){
  int number_count = (int)vect.size();

  double minimum_value = min();
  double maximum_value = max();
  double bin_width = (maximum_value - minimum_value) / bins;

  vector<int> bin_counts(bins, 0);
  if (maximum_value == minimum_value) {
    bin_counts[0] = number_count;
  } else {
    for (int i = 0; i < number_count; i++) {
      int bin_index;

      bin_index = (int)((vect[i] - minimum_value) / bin_width);

      if (bin_index == bins) {
        bin_index = bins - 1;
      }

      bin_counts[bin_index] = bin_counts[bin_index] + 1;
    }
  }
  int maximum_count = bin_counts[0];

  for (int i = 1; i < bins; i++) {
    if (bin_counts[i] > maximum_count) {
      maximum_count = bin_counts[i];
    }
  }

  for (int level = maximum_count; level >= 1; level--) {
    for (int i = 0; i < bins; i++) {
      if (bin_counts[i] >= level) {
        cout << "*** ";
      } else {
        cout << "    ";
      }
    }

    cout << endl;
  }
}
