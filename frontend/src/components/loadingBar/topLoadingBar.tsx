import React, { useState } from 'react';
import LoadingBar from 'react-top-loading-bar';

const TopLoadingBar = ({ progress, setProgress }: any) => {
  return (
    <div className="topLoadingBar">
      <LoadingBar
        color="#fff"
        progress={progress}
        onLoaderFinished={() => setProgress(0)}
      />
    </div>
  );
};

export default TopLoadingBar;
