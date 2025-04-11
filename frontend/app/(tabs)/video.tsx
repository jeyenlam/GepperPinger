import { Image, StyleSheet, Text, View } from 'react-native';
import { useEffect, useState } from 'react';
import CustomScreenContainer from '@/components/CustomScreenContainer';

export default function Video() {
  const [image, setImage] = useState<string | null>(null);
    
  useEffect(() => {
    const ws = new WebSocket(`ws://${process.env.EXPO_PUBLIC_RASPBERRY_PI_IP_ADDRESS}:8000/video_feed`);

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const base64Image = `data:image/jpeg;base64,${data.image}`;
      setImage(base64Image);
    };

    ws.onerror = (error) => {
      console.log('WebSocket Error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <CustomScreenContainer title='Monitor'>
      {image ? (
        <Image
          source={{ uri: image }}
          className='w-full h-1/2'
        />
      ) : (
        <Text>Waiting for video...</Text>
      )}

    </CustomScreenContainer>
  );
}

const styles = StyleSheet.create({
  view: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  video: {
    width: 500, // fit ip14 perfectly
    height: 400,
    transform: [{ rotate: '90deg' }], // Use rotate to rotate the image by 90 degrees
    aspectRatio: 16 / 9,
  }
});
