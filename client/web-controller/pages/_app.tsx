import '../styles/globals.scss';
import type { AppProps } from 'next/app';
import Head from 'next/head';

import styles from './_app.module.scss';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <div className={styles.container}>
        <Head>
          <title>Lunabot Web Controller</title>
          <meta
            name="description"
            content="The Lunabot web controller, allow you to control your bot throught the internet"
          />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <main className={styles.main}>
          <Component {...pageProps} />
        </main>
      </div>
    </>
  );
}

export default MyApp;
