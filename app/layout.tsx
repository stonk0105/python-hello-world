import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Python Hello World with Next.js',
  description: 'Next.js frontend with Python API backend',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body>{children}</body>
    </html>
  )
}