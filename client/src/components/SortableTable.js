import { useEffect } from 'react';
import { Table } from 'react-bootstrap';
import { ArrowUp, ArrowDown } from 'react-bootstrap-icons';
import { useTable, useSortBy, useFilters, useGlobalFilter } from 'react-table';
import TableFilter from './TableFilter'

const SortableTable = (props) => {
 const { 
    data,
    columns,
    onRowClick,
    tdStyle,
    trStyle,
    thStyle,
    onTdClicks,
    tableSize,
    displayHeader,
    rowPointer,
    setPreGlobalFilteredRows,
    setTableState,
    setSetGlobalFilter,
    hideGlobalFilter,
    hideInfinteGlobalFilter,
    searchWidth,
    searchOverlay,
    tableHeight
  } = props;

  const {
   getTableProps,
   getTableBodyProps,
   headerGroups,
   rows,
   prepareRow,
   state,
   preGlobalFilteredRows,
   setGlobalFilter,
  } = useTable({
    columns,
    data
  }, useFilters, useGlobalFilter, useSortBy)
  let rowStyle = []
  if (trStyle){
    rowStyle = {
      fontSize: "14px"
    }
  }
  if (rowPointer){
    rowStyle.cursor = "pointer"
  }
  let sWidth = 6;
  if (searchWidth){
    sWidth = searchWidth;
  }

  useEffect(() => {
    if(hideInfinteGlobalFilter === false){
      setPreGlobalFilteredRows(preGlobalFilteredRows)
      setTableState(state)
      setSetGlobalFilter({
        fn: setGlobalFilter
      })
    }
  }, [hideInfinteGlobalFilter, preGlobalFilteredRows, setGlobalFilter, setTableState, setPreGlobalFilteredRows, state, setSetGlobalFilter])

  const constructRow = row => {
   prepareRow(row);
   const { key, ...restRowProps } = row.getRowProps();
   return (
     <tr 
      key={key}
      id={`tableRow${row.id}`}
      style={rowStyle}
      {...restRowProps}
      onMouseDown={() => {
        if(onRowClick){
          onRowClick(row);
        }
      }}
    >
       {row.cells.map(cell => {
         const { key, ...restCellProps } = cell.getCellProps();
         return (
           <td 
            key={key}
            style={tdStyle}
            {...restCellProps}
            onMouseDown={() => {
              if(onTdClicks && Object.keys(onTdClicks).includes(cell.column.id)){
                return onTdClicks[cell.column.id](cell);
              }
            }}
            >
                <><div className="sortable-table">{cell.render('Cell')}</div></>
           </td>
         )
       })}
     </tr>
   )
  }

  let style = {}
  if (tableHeight){
    style.height = `${tableHeight}px`
    style.fontWeight = "thin"
  }
  
  return (
    <>
      {!hideGlobalFilter &&
        <TableFilter
          searchOverlay={searchOverlay}
          sWidth={sWidth}
          preGlobalFilteredRows={preGlobalFilteredRows}
          globalFilter={state.globalFilter}
          setGlobalFilter={setGlobalFilter}
        />
      }
      <Table style={style} size={tableSize ? tableSize : "sm"} responsive {...getTableProps()} hover>
        {displayHeader !== false &&
        <thead>
           {headerGroups.map((headerGroup,index) => (
             <tr {...headerGroup.getHeaderGroupProps()} key={index}>
               {
               headerGroup.headers.map((column, index) => {
                if (column.hideHeader){
                  return null;
                }
                return (
                  <th key={index} {...column.getHeaderProps(column.getSortByToggleProps())} style={thStyle}>
                   {column.render('Header')}
                   <span>
                    {column.isSorted
                      ? column.isSortedDesc
                        ? <ArrowDown className="ml-2"/>
                        : <ArrowUp className="ml-2"/>
                      : ''}
                  </span>
                 </th>
                )
               })}
             </tr>
           ))}   
         </thead>
        }
        <tbody {...getTableBodyProps()}>
         {rows.map(row => {
           return constructRow(row)
         })}
       </tbody>
      </Table>
    </>
  );
};
export default SortableTable;