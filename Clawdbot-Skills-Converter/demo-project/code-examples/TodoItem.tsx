// src/components/TodoItem.tsx
// 使用 test-driven-development 技能开发的组件

import { useState } from 'react'

interface TodoItemProps {
  id: string
  text: string
  completed: boolean
  onToggle: (id: string) => void
  onDelete: (id: string) => void
}

export function TodoItem({ id, text, completed, onToggle, onDelete }: TodoItemProps) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = () => {
    setIsDeleting(true)
    setTimeout(() => {
      onDelete(id)
    }, 200)
  }

  return (
    <div
      className={`flex items-center gap-3 p-4 rounded-lg shadow-sm transition-all duration-200 ${
        isDeleting ? 'opacity-0 scale-95' : 'opacity-100 scale-100'
      } ${completed ? 'bg-gray-50 dark:bg-gray-800/50' : 'bg-white dark:bg-gray-800'}`}
    >
      <label className="flex items-center gap-3 flex-1 cursor-pointer group">
        <input
          type="checkbox"
          checked={completed}
          onChange={() => onToggle(id)}
          className="w-5 h-5 text-blue-500 rounded border-gray-300 focus:ring-blue-500 cursor-pointer"
          aria-label={`Mark "${text}" as ${completed ? 'incomplete' : 'complete'}`}
        />
        <span
          className={`flex-1 transition-all duration-200 font-medium ${
            completed
              ? 'line-through text-gray-500 dark:text-gray-400'
              : 'text-gray-900 dark:text-white'
          }`}
        >
          {text}
        </span>
      </label>
      <button
        onClick={handleDelete}
        className="px-3 py-1.5 text-sm font-medium text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all duration-200 opacity-0 group-hover:opacity-100 focus:opacity-100"
        aria-label={`Delete "${text}"`}
      >
        删除
      </button>
    </div>
  )
}
