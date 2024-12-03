program day01
    implicit none

    integer, parameter :: num_cols = 2
    integer, allocatable, dimension(:,:) :: input_data
    integer :: num_rows, solution_1, solution_2

    ! Test data
    call load_data("test_input.txt", input_data, num_rows, num_cols)

    solution_1 = solve_part1(input_data)
    call assert_equal(solution_1, 11)

    solution_2 = solve_part2(input_data)
    call assert_equal(solution_2, 31)

    ! Reset the allocation
    deallocate(input_data)

    call load_data("input.txt", input_data, num_rows, num_cols)

    solution_1 = solve_part1(input_data)

    print *, "The solution to part 1 is ", solution_1
    print *

    solution_2 = solve_part2(input_data)

    print *, "The solution to part 2 is ", solution_2
    print *

contains

    subroutine load_data(filename, input_data, num_rows, num_cols)
        !
        ! Load data into a 2d integer array from a file with unknown number of rows
        ! and known number of columns.
        !
        character(*), intent(in) :: filename
        integer, intent(out), allocatable, dimension(:,:) :: input_data
        integer, intent(out) :: num_rows
        integer, intent(in) :: num_cols

        integer, parameter :: file_handle = 2

        character(1000) :: row_buffer
        integer :: i, j, stat

        ! Open the file for reading
        open(unit=file_handle, file=filename, status="old")

        ! First, we need to read all the rows in the file to count them
        num_rows = 0
        do while(.TRUE.)
            read (2, *, iostat=stat) row_buffer
            if (stat /= 0) exit  ! break the loop once we run out of rows
            num_rows = num_rows + 1
        end do

        ! Go back to the beginning of the file
        rewind(file_handle)

        ! Now, we allocate the memory for the array
        allocate(input_data(num_rows, num_cols))

        ! Read all the rows into the array
        do i=1,num_rows
            read (2, *) (input_data(i,j), j=1,num_cols)
        end do

        ! Make sure we close the file
        close(file_handle)

    end subroutine load_data

    function solve_part1(input_data) result (x)
        integer, intent(in), dimension(:,:) :: input_data

        integer, dimension(size(input_data, 1)) :: left, right

        integer :: x
        integer :: num_rows, num_cols
        integer :: i

        num_rows = size(input_data, 1)
        num_cols = size(input_data, 2)

        left = input_data(:,1)
        right = input_data(:,2)

        call quicksort(left)
        call quicksort(right)

        x = 0
        do i = 1,num_rows
            x = x + abs(right(i) - left(i))
        end do
    end function solve_part1

    function solve_part2(input_data) result (x)
        integer, intent(in), dimension(:,:) :: input_data

        integer, dimension(size(input_data, 1)) :: left, right

        integer :: x
        integer :: num_rows, i, j

        num_rows = size(input_data, 1)

        left = input_data(:,1)
        right = input_data(:,2)

        x = 0
        do i=1,num_rows
            do j=1,num_rows
                if (left(i) == right(j)) then
                    x = x + left(i)
                end if
            end do
        end do
    end function solve_part2

    recursive subroutine quicksort(a, firstin, lastin)
        !
        ! Modified from: https://gist.github.com/t-nissie/479f0f16966925fa29ea
        !
        integer :: a(:)
        real :: x, t
        integer  :: first, last
        integer, optional :: firstin, lastin
        integer :: i, j

        if (present(firstin)) then
            first = firstin
        else
            first = 1
        end if

        if (present(lastin)) then
            last = lastin
        else
            last = size(a,1)
        end if

        x = a( (first+last) / 2 )
        i = first
        j = last
        do
            do while (a(i) < x)
                i = i + 1
            end do
         do while (x < a(j))
            j=j-1
         end do
         if (i >= j) exit
         t = a(i);  a(i) = a(j);  a(j) = t
         i=i+1
         j=j-1
      end do
      if (first < i-1) call quicksort(a, first, i-1)
      if (j+1 < last)  call quicksort(a, j+1, last)
    end subroutine quicksort

    subroutine assert_equal(actual, expected)
        !
        ! Exit early if the two integer values are not equal.
        !
        integer, intent(in) :: actual, expected

        if (actual .ne. expected) then
            print *, "ASSERTION FAILED, ", actual, "!=", expected
            call exit(1)
        end if
    end subroutine assert_equal


end program day01
