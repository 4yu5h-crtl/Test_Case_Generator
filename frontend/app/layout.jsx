import './globals.css'

export const metadata = {
  title: 'AI-Powered Test Generation',
  description: 'Streamline testing with intelligent automation',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-800">
        {children}
      </body>
    </html>
  )
}


