import React from 'react';
import {View, StyleSheet, ScrollView} from 'react-native';
import {Title, Card, Paragraph, Button} from 'react-native-paper';

const HomeScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <Title style={styles.title}>Pediatric Health Assistant</Title>
      <Card style={styles.card}>
        <Card.Content>
          <Title>Welcome to Parent Forum</Title>
          <Paragraph>
            A safe space for parents to share experiences and support each other
            through childhood health journeys.
          </Paragraph>
        </Card.Content>
        <Card.Actions>
          <Button mode="contained" onPress={() => {}}>
            Start Chat
          </Button>
        </Card.Actions>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title>Quick Access</Title>
          <View style={styles.buttonContainer}>
            <Button mode="outlined" style={styles.button} onPress={() => {}}>
              Growth Charts
            </Button>
            <Button mode="outlined" style={styles.button} onPress={() => {}}>
              Forum
            </Button>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    margin: 20,
    color: '#2c3e50',
  },
  card: {
    margin: 10,
    elevation: 4,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  button: {
    marginHorizontal: 5,
  },
});

export default HomeScreen;