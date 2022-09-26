import dynamic from 'next/dynamic';
import React from 'react';

const NoSsrComponent = (props: any) => <>{props.children}</>;

export const NoSsr = dynamic(() => Promise.resolve(NoSsrComponent), {
  ssr: false,
});
