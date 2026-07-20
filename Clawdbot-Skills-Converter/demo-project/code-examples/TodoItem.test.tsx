// src/components/TodoItem.test.tsx
// 使用 test-driven-development 技能的 RED-GREEN-REFACTOR 流程

import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { TodoItem } from './TodoItem'

describe('TodoItem', () => {
  // RED 1: 基础渲染测试
  it('should render todo text', () => {
    render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />
    )
    expect(screen.getByText('Learn React')).toBeInTheDocument()
  })

  // GREEN 1: 实现通过
  it('should show completed state with strikethrough', () => {
    render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={true}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />
    )
    const text = screen.getByText('Learn React')
    expect(text).toHaveClass('line-through')
  })

  // RED 2: 交互测试
  it('should call onToggle when checkbox is clicked', () => {
    const onToggle = vi.fn()
    render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={onToggle}
        onDelete={vi.fn()}
      />
    )

    const checkbox = screen.getByRole('checkbox')
    fireEvent.click(checkbox)

    expect(onToggle).toHaveBeenCalledWith('1')
    expect(onToggle).toHaveBeenCalledTimes(1)
  })

  // GREEN 2: 实现通过
  it('should call onDelete when delete button is clicked', () => {
    const onDelete = vi.fn()
    render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={vi.fn()}
        onDelete={onDelete}
      />
    )

    const deleteButton = screen.getByText('删除')
    fireEvent.click(deleteButton)

    setTimeout(() => {
      expect(onDelete).toHaveBeenCalledWith('1')
    }, 250)
  })

  // RED 3: 可访问性测试
  it('should have proper accessibility labels', () => {
    render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />
    )

    const checkbox = screen.getByRole('checkbox', {
      name: /Mark "Learn React" as complete/
    })
    const deleteButton = screen.getByRole('button', {
      name: /Delete "Learn React"/
    })

    expect(checkbox).toBeInTheDocument()
    expect(deleteButton).toBeInTheDocument()
  })

  // GREEN 3: 实现通过
  it('should handle deletion animation', () => {
    const onDelete = vi.fn()
    const { rerender } = render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={vi.fn()}
        onDelete={onDelete}
      />
    )

    const container = screen.getByRole('listitem')?.parentElement
    expect(container).toHaveClass('opacity-100', 'scale-100')

    fireEvent.click(screen.getByText('删除'))

    expect(container).toHaveClass('opacity-0', 'scale-95')
  })

  // REFACTOR: 优化代码结构
  it('should have correct styling for different states', () => {
    const { rerender } = render(
      <TodoItem
        id="1"
        text="Learn React"
        completed={false}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />
    )

    const container = screen.getByRole('listitem')?.parentElement
    expect(container).toHaveClass('bg-white', 'dark:bg-gray-800')

    rerender(
      <TodoItem
        id="1"
        text="Learn React"
        completed={true}
        onToggle={vi.fn()}
        onDelete={vi.fn()}
      />
    )

    expect(container).toHaveClass('bg-gray-50', 'dark:bg-gray-800/50')
  })
})

/*
TDD 流程总结:

1. RED: 编写失败测试
   - 识别需要的功能
   - 编写测试用例
   - 确认测试失败

2. GREEN: 编写最小实现
   - 实现最简单的代码使测试通过
   - 不考虑代码质量，只求通过

3. REFACTOR: 重构优化
   - 优化代码结构
   - 提高可读性
   - 保持测试通过
*/
