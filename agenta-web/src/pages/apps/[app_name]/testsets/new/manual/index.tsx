import React, { useState, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';

import { Button, Input, Typography } from 'antd';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { PlusOutlined } from '@ant-design/icons';

export default function Manual() {
    const [rowData, setRowData] = useState([
        { column1: "data1", column2: "data2", column3: "data3" },
        { column1: "data1", column2: "data2", column3: "data3" },
        { column1: "data1", column2: "data2", column3: "data3" }
    ]);

    const [columnDefs, setColumnDefs] = useState([
        { field: 'column1' },
        { field: 'column2' },
        { field: 'column3' }
    ]);

    const [inputValues, setInputValues] = useState(columnDefs.map(col => col.field));
    const gridRef = useRef(null);

    const handleInputChange = (index, event) => {
        const values = [...inputValues];
        values[index] = event.target.value;
        setInputValues(values);
    }

    const updateTable = () => {
        const newColumnDefs = inputValues.map((value, index) => {
            return { field: value || columnDefs[index]?.field || `newColumn${index}` };
        });

        const keyMap = columnDefs.reduce((acc, colDef, index) => {
            acc[colDef.field] = newColumnDefs[index].field;
            return acc;
        }, {});

        const newRowData = rowData.map(row => {
            const newRow = {};
            for (let key in row) {
                newRow[keyMap[key]] = row[key];
            }
            return newRow;
        });

        setColumnDefs(newColumnDefs);
        setRowData(newRowData);
        if (gridRef.current) {
            gridRef.current.setColumnDefs(newColumnDefs);
        }
    };

    const defaultColDef = {
        flex: 1,
        minWidth: 100,
        editable: true,
    };

    const onAddRow = () => {
        const newRow = {};
        columnDefs.forEach(colDef => {
            newRow[colDef.field] = '';
        });
        setRowData([...rowData, newRow]);
    };

    const onAddColumn = () => {
        setInputValues([...inputValues, `column${columnDefs.length + 1}`]);
        setColumnDefs([...columnDefs, { field: `column${columnDefs.length + 1}` }]);
    };

    const onSaveData = () => {
        console.log(rowData);
    };

    return (
        <div>
            <Typography.Title level={5} style={{ marginBottom: '20px' }}>
                Create a new Test Set
            </Typography.Title>

            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', marginBottom: '20px' }}>
                {columnDefs.map((colDef, index) => (
                    <div key={index} style={{ marginRight: '10px' }}>
                        <Input
                            key={index}
                            value={inputValues[index]}
                            onChange={event => handleInputChange(index, event)}
                        />
                    </div>
                ))}

                <Button onClick={onAddColumn} style={{ marginRight: '10px' }}><PlusOutlined /></Button>
                <Button onClick={updateTable} type="primary">Update Columns names</Button>
            </div>

            <div className="ag-theme-alpine" style={{ height: 500 }}>
                <AgGridReact
                    onGridReady={params => gridRef.current = params.api}
                    rowData={rowData}
                    columnDefs={columnDefs}
                    defaultColDef={defaultColDef}
                    singleClickEdit={true}
                    statusBar={{
                        statusPanels: [
                            {
                                statusPanel: 'agAggregationComponent',
                                statusPanelParams: {
                                    aggFuncs: ['sum'],
                                },
                            },
                        ],
                    }}
                />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
                <Button onClick={onAddRow} >Add Row</Button>
                <Button onClick={onSaveData} type="primary">Save Test Set</Button>
            </div>
        </div>
    );
};
