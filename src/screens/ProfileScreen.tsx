import React from 'react';
import {View, StyleSheet, ScrollView} from 'react-native';
import {Title, Button, Avatar, List} from 'react-native-paper';

const ProfileScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Avatar.Icon size={80} icon="account" />
        <Title style={styles.username}>Username</Title>
      </View>

      <List.Section>
        <List.Item
          title="My Posts"
          left={props => <List.Icon {...props} icon="post" />}
          onPress={() => {}}
        />
        <List.Item
          title="Notifications"
          left={props => <List.Icon {...props} icon="bell" />}
          onPress={() => {}}
        />
        <List.Item
          title="Settings"
          left={props => <List.Icon {...props} icon="cog" />}
          onPress={() => {}}
        />
      </List.Section>

      <Button mode="contained" style={styles.logoutButton} onPress={() => {}}>
        Logout
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  username: {
    marginTop: 10,
  },
  logoutButton: {
    margin: 20,
  },
});

export default ProfileScreen;