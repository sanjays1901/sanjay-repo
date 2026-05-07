import React from 'react';

const SourceCitation = ({ source }) => {
  // Backend returns: { source: { source: "file.pdf", ... }, distance: 0.31 }
  return (
    <div className="source-chip" title={`Relevance distance: ${source.distance?.toFixed(4)}`}>
      📄 {source.source?.source || 'Unknown Source'}
    </div>
  );
};
export default SourceCitation;