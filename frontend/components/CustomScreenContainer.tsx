import React, { ReactNode, useState } from 'react';
import { View, Text, StyleSheet, Image, ScrollView, RefreshControl } from 'react-native';

interface CustomScreenContainerProps {
  title?: string;
  children?: ReactNode;
}

const CustomScreenContainer: React.FC<CustomScreenContainerProps> = ({ title, children }) => {
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = () => {
    setRefreshing(true);
    setTimeout(() => {
      setRefreshing(false);
    }, 1500);
  };

  return (
    <View style={styles.container} >
      <ScrollView
      className='mt-20'
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={{ paddingBottom: 40 }}
        showsVerticalScrollIndicator={false}
      >
        {title && <Text style={styles.title}>{title}</Text>}
        {children}        
      </ScrollView>


    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    display: 'flex',
    flexDirection: 'column',
    paddingTop: 60,
    padding: 16,
    height: '100%',
    overflow: 'scroll',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    paddingBottom: 16,
  },
});

export default CustomScreenContainer;