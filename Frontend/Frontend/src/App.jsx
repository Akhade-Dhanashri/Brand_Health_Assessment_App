import React, { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

const sampleData = [
  { category: 'Awareness', score: 12 },
  { category: 'Perception', score: 9 },
  { category: 'Consideration', score: 6 },
  { category: 'Purchase', score: 10 }
]

export default function App() {
  const [data] = useState(sampleData)

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">Brand Health Assessment</h1>
      <BarChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="category" />
        <YAxis domain={[0, 15]} />
        <Tooltip />
        <Legend />
        <Bar dataKey="score" fill="#8884d8" />
      </BarChart>
    </div>
  )
}
