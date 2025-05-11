import React, {useState} from 'react';
import {View, StyleSheet, ScrollView, Dimensions} from 'react-native';
import {Title, Button, TextInput} from 'react-native-paper';
import {LineChart} from 'react-native-chart-kit';

const GrowthScreen = () => {
  const [gender, setGender] = useState('Male');
  const [age, setAge] = useState('0');
  const [weight, setWeight] = useState('0');
  const [height, setHeight] = useState('0');

  const chartConfig = {
    backgroundGradientFrom: '#ffffff',
    backgroundGradientTo: '#ffffff',
    color: (opacity = 1) => `rgba(74, 111, 165, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
  };

  return (
    <ScrollView style={styles.container}>
      <Title style={styles.title}>Growth Chart Visualizer</Title>

      <View style={styles.inputContainer}>
        <Button
          mode={gender === 'Male' ? 'contained' : 'outlined'}
          onPress={() => setGender('Male')}
          style={styles.genderButton}>
          Male
        </Button>
        <Button
          mode={gender === 'Female' ? 'contained' : 'outlined'}
          onPress={() => setGender('Female')}
          style={styles.genderButton}>
          Female
        </Button>
      </View>

      <TextInput
        label="Age (months)"
        value={age}
        onChangeText={setAge}
        keyboardType="numeric"
        style={styles.input}
      />
      <TextInput
        label="Weight (kg)"
        value={weight}
        onChangeText={setWeight}
        keyboardType="numeric"
        style={styles.input}
      />
      <TextInput
        label="Height (cm)"
        value={height}
        onChangeText={setHeight}
        keyboardType="numeric"
        style={styles.input}
      />

      <Button mode="contained" style={styles.plotButton}>
        Plot Growth Charts
      </Button>

      {/* Sample Chart */}
      <LineChart
        data={{
          labels: ['0', '6', '12', '18', '24'],
          datasets: [
            {
              data: [3, 6, 8, 10, 12],
            },
          ],
        }}
        width={Dimensions.get('window').width - 20}
        height={220}
        chartConfig={chartConfig}
        bezier
        style={styles.chart}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    padding: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    margin: 20,
  },
  inputContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  genderButton: {
    width: '45%',
  },
  input: {
    marginBottom: 10,
  },
  plotButton: {
    marginVertical: 20,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
});

export default GrowthScreen;