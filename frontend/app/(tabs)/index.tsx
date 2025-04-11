import CustomScreenContainer from '@/components/CustomScreenContainer';
import { useState } from 'react';
import { Image, StyleSheet, View, Text} from 'react-native';
import { activities } from '@/constants/Data';

export default function HomeScreen() {
  const [GingerActivity, setGingerActivity] = useState('Sleeping');
  const [PepperActivity, setPepperActivity] = useState('Sleeping');

  return (
    <CustomScreenContainer title='Home'>
      <View>  
        <Text>Ginger's Activity</Text>
        {
          activities.map((activity, index) => 
            GingerActivity === activity.title && 
            <Image 
              source={typeof activity.imageUrl === 'string' ? { uri: activity.imageUrl } : activity.imageUrl}
              key={index}
              style={
                { 
                  width: 100,
                  height: 100 
                }} 
            /> )
        }
      </View>
      <View>
        <Text>Pepper's Activity</Text>
        {
          activities.map((activity, index) => 
            GingerActivity === activity.title && 
            <Image 
              source={typeof activity.imageUrl === 'string' ? { uri: activity.imageUrl } : activity.imageUrl}
              key={index}
              style={
                { 
                  width: 100,
                  height: 100 
                }} 
            /> )
        }
      </View>

    </CustomScreenContainer>
  );
}
