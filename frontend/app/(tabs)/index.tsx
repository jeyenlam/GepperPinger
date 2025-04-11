import CustomScreenContainer from '@/components/CustomScreenContainer';
import { useState } from 'react';
import { Image, View, Text} from 'react-native';
import { activities } from '@/constants/Data';
import { UserPen } from 'lucide-react-native';
import "@/global.css"

interface Dog {
  name: string;
  age: number;
  breed: string;
  activity: string;
  lastSeenAt: Date;
  imageUrl: string;
}


export default function HomeScreen() {
  const myDogs : Dog[] = [
    {
      name: 'Ginger',
      age: 1,
      breed: 'Shih Tzu Mix',
      activity: 'Sleeping',
      lastSeenAt: new Date(),
      imageUrl: '/',
    }, 
    {
      name: 'Pepper',
      age: 1,
      breed: 'Shih Tzu Mix',
      activity: 'Sleeping',
      lastSeenAt: new Date(),
      imageUrl: '/',
    }
  ]

  return (
    <CustomScreenContainer title='Home'>
      <Text className='-top-8 self-end'>
        <UserPen color="black" size={25} />
      </Text>
      {myDogs.map((dog, index) => (
        <View key={index} className='flex flex-col items-center justify-center'>
          <Image source={typeof dog.imageUrl === 'string' ? { uri: dog.imageUrl } : dog.imageUrl} className='w-1/4 h-1/4'/>
          
          <View className='ml-2'>
            <Text className='text-lg font-bold'>{dog.name}</Text>
            <Text>Age: {dog.age}</Text>
            <Text>Breed: {dog.breed}</Text>
            <Text>Last seen: {dog.lastSeenAt.toLocaleTimeString()}</Text>
          </View>
          <View className='flex justify-center items-center'>  
            <View className='flex flex-row items-center'>
              <Text className='relative text-5xl text-green-600 z-10'>•</Text>
              <Text className='absolute animate-ping text-[5rem] text-green-600 delay-1000 duration-1000 z-0'>•</Text>
              <Text className=''>Ginger is {dog.activity} 💤</Text>
            </View>
        
            {
              activities.map((activity, index) => 
                dog.activity === activity.title && 
                <Image key={index} source={typeof activity.imageUrl === 'string' ? { uri: activity.imageUrl } : activity.imageUrl}/> )
            }
          </View>
          
        </View>
      ))}

    </CustomScreenContainer>
  );
}
