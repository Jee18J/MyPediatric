import React, {useState} from 'react';
import {View, StyleSheet, ScrollView} from 'react-native';
import {
  Title,
  Card,
  Button,
  TextInput,
  Chip,
  Portal,
  Modal,
  List,
} from 'react-native-paper';

const CONDITIONS = [
  'Common Cold',
  'Gastroenteritis',
  'Asthma',
  'Meningitis',
  'Scarlet Fever',
  'Eczema',
  'Croup',
  'Type 1 Diabetes',
  'Bronchiolitis',
  'Influenza',
  'Pneumonia',
  'Allergies',
  'Ear Infection',
  'Skin Rash',
  'Diarrhea',
  'Fever',
  'Viral Illness',
];

const ForumScreen = () => {
  const [visible, setVisible] = useState(false);
  const [selectedCondition, setSelectedCondition] = useState('');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  return (
    <ScrollView style={styles.container}>
      <Title style={styles.title}>Parent Forum</Title>

      <Button
        mode="contained"
        style={styles.createButton}
        onPress={() => setVisible(true)}>
        Create New Post
      </Button>

      <Portal>
        <Modal
          visible={visible}
          onDismiss={() => setVisible(false)}
          contentContainerStyle={styles.modal}>
          <Title>Create New Post</Title>
          <TextInput
            label="Title"
            value={title}
            onChangeText={setTitle}
            style={styles.input}
          />
          <TextInput
            label="Content"
            value={content}
            onChangeText={setContent}
            multiline
            numberOfLines={4}
            style={styles.input}
          />
          <List.Section title="Select Condition">
            <ScrollView style={styles.conditionList}>
              {CONDITIONS.map(condition => (
                <Chip
                  key={condition}
                  selected={selectedCondition === condition}
                  onPress={() => setSelectedCondition(condition)}
                  style={styles.chip}>
                  {condition}
                </Chip>
              ))}
            </ScrollView>
          </List.Section>
          <View style={styles.buttonContainer}>
            <Button onPress={() => setVisible(false)}>Cancel</Button>
            <Button mode="contained" onPress={() => {}}>
              Post
            </Button>
          </View>
        </Modal>
      </Portal>

      {/* Sample Posts */}
      <Card style={styles.card}>
        <Card.Title title="Sample Post" subtitle="Common Cold • 2h ago" />
        <Card.Content>
          <Title>My experience with treating cold</Title>
        </Card.Content>
        <Card.Actions>
          <Button>Comment</Button>
          <Button>Share</Button>
        </Card.Actions>
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
  },
  createButton: {
    margin: 10,
  },
  modal: {
    backgroundColor: 'white',
    padding: 20,
    margin: 20,
    borderRadius: 10,
  },
  input: {
    marginVertical: 10,
  },
  conditionList: {
    maxHeight: 150,
  },
  chip: {
    margin: 4,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 20,
  },
  card: {
    margin: 10,
  },
});

export default ForumScreen;