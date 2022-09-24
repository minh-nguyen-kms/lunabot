import type { NextPage } from 'next';
import { BotController } from '../features/bot-controller/bot-controller';
const Home: NextPage = () => {
  return (
    <>
      <BotController />
    </>
  );
};

export default Home;
