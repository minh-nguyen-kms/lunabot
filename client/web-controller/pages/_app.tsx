import '../styles/globals.scss';
import type { AppProps } from 'next/app';
import Head from 'next/head';

import './_app.scss';
import styles from './_app.module.scss';
import { FullScreenController } from '../features/bot-controller/full-screen-controller/FullScreenController';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Lunabot Web Controller</title>
        <meta
          name="description"
          content="The Lunabot web controller, allow you to control your bot throught the internet"
        />
        <link rel="icon" href="/favicon.ico" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
        />
      </Head>

      <main id="main" className={styles.main}>
        <Component {...pageProps} />
      </main>
      <FullScreenController targetId="main" />
    </>
  );
}

export default MyApp;
