import FilterizrOptions from '../FilterizrOptions/index';
import { Dictionary, Position } from '../types/interfaces/index';
export declare const makeInitialStyles: (options: FilterizrOptions) => object;
export declare const makeFilteringStyles: (targetPosition: Position, cssOptions: Dictionary) => object;
export declare const makeTransitionStyles: (index: number, options: FilterizrOptions) => object;
