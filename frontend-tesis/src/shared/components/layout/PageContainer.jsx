import React from 'react';

/**
 * PageContainer provides the standard centered layout with padding
 * for most dashboard pages. Pages like 'Tutor' that need full width
 * should NOT use this container.
 */
const PageContainer = ({ children, className = "" }) => {
  return (
    <div className={`max-w-[1200px] mx-auto w-full p-6 lg:p-12 ${className}`}>
      {children}
    </div>
  );
};

export default PageContainer;
