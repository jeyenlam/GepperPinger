import { PropsWithChildren, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';

export function Collapsible({ children, title }: PropsWithChildren & { title: string }) {
  const [isOpen, setIsOpen] = useState(true);
  const theme = useColorScheme() ?? 'light';

  return (
    <View className='mt-10'>
      <TouchableOpacity
        className='flex flex-row gap-2 items-center'
        onPress={() => setIsOpen((value) => !value)}
        activeOpacity={0.8}
      >
        <Text className='font-bold text-lg'>{title}</Text>
        <IconSymbol
          name="chevron.up"
          size={14}
          weight="medium"
          color={theme === 'light' ? Colors.light.icon : Colors.dark.icon}
          style={{ transform: [{ rotate: isOpen ? '180deg' : '0deg' }] }}
        />

      </TouchableOpacity>
      {isOpen && <View>{children}</View>}
    </View>
  );
}