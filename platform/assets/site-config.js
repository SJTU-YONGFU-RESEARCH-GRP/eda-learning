/**
 * Site integration keys for EDA Algorithms Platform.
 * Course media loads from monorepo courses/ via course-media/ on localhost.
 */
window.SITE_CONFIG = {
  brand: "EDA Algorithms Platform",
  ga4MeasurementId: "",
  feedbackIssuesUrl: "",
  simulatorUrl: "",
  githubOrg: "universal-verification-methodology",
  mediaBranch: "main",
  mediaCdn: "jsdelivr",
  /**
   * "auto" — local course-media on localhost, CDN elsewhere
   * "local" — always /course-media/<repo>/…
   * "cdn" — always jsDelivr/raw (needs published course repo)
   */
  mediaSource: "auto",
  progressKey: "eda.progress.v1",
};
