import CustomScreenContainer from '@/components/CustomScreenContainer';
import { Image, View, Text, ImageBackground} from 'react-native';
import { Bone, Dog, UserPen } from 'lucide-react-native';
import "@/global.css"
import { Collapsible } from '@/components/Collapsible';

interface Dog {
  name: string;
  age: number;
  breed: string;
  activity: string;
  lastSeenAt: Date;
  weight: number;
  imageUrl: string;
}

export default function HomeScreen() {
  const myDogs : Dog[] = [
    {
      name: 'Ginger',
      age: 1,
      breed: 'Shih Tzu Mix',
      weight: 13,
      activity: 'Sleeping',
      lastSeenAt: new Date(),
      imageUrl: require('@/assets/images/ginger.jpg'),
    }, 
    {
      name: 'Pepper',
      age: 1,
      breed: 'Shih Tzu Mix',
      weight: 11,
      activity: 'Playing',
      lastSeenAt: new Date(),
      imageUrl: require('@/assets/images/pepper.jpg'),
    }
  ]


  return (
    <CustomScreenContainer title='Home'>
      <Text className='self-end'>
        <UserPen color="black" size={25} />
      </Text>

      <View className='mb-10 flex flex-row items-center gap-2'>
        {myDogs.map((dog, index) => (
          <View key={index}>
            <Image
              source={
                typeof dog.imageUrl === 'string'
                  ? { uri: dog.imageUrl }
                  : dog.imageUrl
              }
              className='w-20 h-20 rounded-full border-4 border-[#E6B619]'
            />
            <View className='ml-2'>
              <Text className='text-lg font-bold'>{dog.name}</Text>
            </View>
          </View>
        ))}
      </View>

      <Collapsible title='Profiles'>
        {myDogs.map((dog, index) => (
          <View key={index}>
            <View className='p-2 bg-[#E6B619]/80 rounded-lg mb-2'>
              <Text className='text-lg font-bold'>{dog.name}</Text>
              <Text>{dog.age} year old</Text>
              <Text>{dog.breed}</Text>
              <Text>{dog.weight} lbs</Text>
              <Text>Last seen: {dog.lastSeenAt.toLocaleTimeString()}</Text>
              <Bone color={'black'} size={50} />
            </View>
          </View>
        ))}
        <ImageBackground
          source={require('@/assets/images/ginger.jpg')}
          className="w-full h-32 bg-tra justify-center items-center"
          resizeMode="cover"
          imageStyle={{ opacity: 0.5 }} // directly reduce image opacity

        >

          <Text className="text-white text-xl font-bold">Overlay Text</Text>
        </ImageBackground>
      </Collapsible>

      <Collapsible title='Appoinments'>
        {myDogs.map((dog, index) => (
          <View key={index}>
            <View className='p-2 bg-[#E6B619]/80 rounded-lg mb-2'>
              <Text className='text-lg font-bold'>{dog.name}</Text>
              <Text>{dog.age} year old</Text>
              <Text>{dog.breed}</Text>
              <Text>{dog.weight} lbs</Text>
              <Text>Last seen: {dog.lastSeenAt.toLocaleTimeString()}</Text>
              <Bone color={'black'} size={50} />
            </View>
          </View>
        ))}
      </Collapsible>
    </CustomScreenContainer>
  );
}
