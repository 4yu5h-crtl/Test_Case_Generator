import { render, screen, fireEvent } from '@testing-library/react'
import React from 'react'
import FileTree from '../components/FileTree'

jest.mock('../lib/backend', () => ({
  fetchRepoFiles: jest.fn(async () => ([
    { path: 'src/index.js', size: 1200 },
    { path: 'src/utils/helpers.js', size: 800 },
  ])),
}))

describe('FileTree', () => {
  it('loads and shows files on click', async () => {
    render(<FileTree owner="owner" repo="repo" />)
    const btn = screen.getByText(/load files/i)
    fireEvent.click(btn)
    expect(await screen.findByText('index.js')).toBeInTheDocument()
    expect(await screen.findByText('helpers.js')).toBeInTheDocument()
  })
})


