import React, { ReactNode } from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface CustomScreenContainerProps {
  title?: string;
  children?: ReactNode;
}

const CustomScreenContainer: React.FC<CustomScreenContainerProps> = ({ title, children }) => {
  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    display: 'flex',
    flexDirection: 'column',
    padding: 16,
    height: '100%',
    overflow: 'scroll',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    paddingTop: 60,
    paddingBottom: 16,
  },
});

export default CustomScreenContainer;