interface Activity {
  title: string;
  imageUrl: string;
}

export const activities: Activity[] = [
  {
    title: 'Sleeping',
    imageUrl: require('../assets/images/activities/sleeping.png')
  },
  {
    title: 'Playing',
    imageUrl: require('../assets/images/activities/playing.png')
  }
]