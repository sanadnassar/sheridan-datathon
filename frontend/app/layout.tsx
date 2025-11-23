// app/layout.tsx
import "./globals.css";
import AnimatedLayout from "./AnimatedLayout"; // <-- we'll create this

export const metadata = {
  title: "HydraX – AI for Sustainable Cities",
  description:
    "AI-powered sustainability tool that helps London measure and visualize rainwater harvesting potential.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="hx-body">
        <AnimatedLayout>{children}</AnimatedLayout>
      </body>
    </html>
  );
}
