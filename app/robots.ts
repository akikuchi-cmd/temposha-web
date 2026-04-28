import type { MetadataRoute } from "next"

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: [
          "Googlebot",
          "Googlebot-Image",
          "Googlebot-News",
          "Googlebot-Video",
          "AdsBot-Google",
          "Mediapartners-Google",
          "Google-InspectionTool",
          "Storebot-Google",
        ],
        allow: "/",
      },
    ],
    sitemap: "https://temposha-web.vercel.app/sitemap.xml",
  }
}
